from django.core.exceptions import ObjectDoesNotExist

from .models import RefbooksVersions


def findRebookVersion(version_query, id):
    """
    Находит выбранную или актуальную версию справочника.
    Вернёт Exception с указанием, если версия или справочник не найдены.
    :param version_query: версия справочника
    :param id: id версии справочника (берётся из дресной строки)
    :return: возвращает Exception или найденную версию справочника
    """
    if version_query is not None:
        try:
            queryset_version = RefbooksVersions.objects.get(rb_id=id, version=version_query)
        except ObjectDoesNotExist:
            raise KeyError("Данная версия справочника не найдена.")
        return queryset_version
    try:
        queryset_version = RefbooksVersions.objects.filter(rb_id=id).latest("date")
    except ObjectDoesNotExist:
        raise KeyError("Указанный справочник отсутствует или не имеет версий!")
    return queryset_version