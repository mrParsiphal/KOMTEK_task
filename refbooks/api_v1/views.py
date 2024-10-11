from datetime import date

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Refbooks, RefbooksVersions, RefbooksElements
from .methods import findRebookVersion


@swagger_auto_schema(method="get", manual_parameters=[
    openapi.Parameter("date", openapi.IN_QUERY, type=openapi.TYPE_STRING)
])
@api_view(["GET"])
def getRebooks(request):
    """
    Получение списка справочников.
    Если указан параметр date, возвращаются только те справочники,
    в которых имеются версии с датой начала действия раннее или равной указанной.

    :param request: входящий запрос
    :return: возвращает Response() со списком значений версий справочника
    """
    date_query = request.GET.get("date", None)
    if date_query is not None:
        queryset = (RefbooksVersions.objects.
                    filter(date__gte=date.fromisoformat(date_query)).
                    values(
                        "rb_id__id",
                        "rb_id__code",
                        "rb_id__name",
                    )).distinct()
        if not queryset:
            return Response({
                "error": "Версии справочников подходящие запросу отсутствуют."
            }, status=status.HTTP_404_NOT_FOUND)
        for row in queryset:
            row["id"] = row.pop("rb_id__id")
            row["code"] = row.pop("rb_id__code")
            row["name"] = row.pop("rb_id__name")
        return Response({"refbooks": queryset}, status=status.HTTP_200_OK)
    queryset = Refbooks.objects.values("id", "code", "name")
    return Response({"refbooks": queryset}, status=status.HTTP_200_OK)


@swagger_auto_schema(method="get", manual_parameters=[
    openapi.Parameter("version", openapi.IN_QUERY, type=openapi.TYPE_STRING)
])
@api_view(["GET"])
def getRebookElements(request, id):
    """
    Получение элементов заданного справочника текущей версии.
    Если указан параметр version, возвращается список элементов указанной версии.

    :param request: входящий запрос
    :param id: id версии справочника (берётся из адресной строки)
    :return: возвращает Response() со списком значений элементов выбранной версии
    """
    version = request.GET.get("version", None)
    try:
        rebook_version = findRebookVersion(version, id)
    except Exception as ex:
        return Response({"error": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    queryset = RefbooksElements.objects.filter(rbv_id__id=rebook_version.id).values("code", "value")
    if not queryset:
        return Response({
            "error": "Елементы подходящие запросу отсутствуют."
        }, status=status.HTTP_404_NOT_FOUND)
    return Response({"elements": queryset}, status=status.HTTP_200_OK)


@swagger_auto_schema(method="get", manual_parameters=[
    openapi.Parameter("code", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("value", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("version", openapi.IN_QUERY, type=openapi.TYPE_STRING)
])
@api_view(["GET"])
def rebookCheckElement(request, id):
    """
    Валидация элемента справочника.
    Параметры адресной строки code и value являются обязательными.

    :param request: входящий запрос
    :param id: id версии справочника (берётся из дресной строки)
    :return: возвращает Response() в виде значения boolean
    """
    code_query = request.GET.get("code", None)
    value_query = request.GET.get("value", None)
    if code_query is None or value_query is None:
        return Response({"error": "Код или значение элемента не указаны."}, status=status.HTTP_400_BAD_REQUEST)
    version = request.GET.get("version", None)
    try:
        rebook_version = findRebookVersion(version, id)
    except Exception as ex:
        return Response({"error": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    return Response(RefbooksElements.objects.filter(
        rbv_id=rebook_version.id,
        code=code_query,
        value=value_query
    ).exists())
