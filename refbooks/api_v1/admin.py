from django.contrib import admin
from .models import Refbooks, RefbooksVersions, RefbooksElements


class VersionsInLine(admin.TabularInline):
    model = RefbooksVersions


class ElementsInLine(admin.TabularInline):
    model = RefbooksElements


@admin.register(Refbooks)
class RefbooksBAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "LastVersion",
        "LastVersionDate"
    ]
    inlines = [
        VersionsInLine,
    ]
    search_fields = ['name', 'pk', ]

    @admin.display(description="Текущая версия")
    def LastVersion(self, obj):
        return RefbooksVersions.objects.filter(rb_id=obj.pk).latest("date")

    @admin.display(description="Дата начала действия версии")
    def LastVersionDate(self, obj):
        last_version = RefbooksVersions.objects.filter(rb_id=obj.pk).latest("date")
        if last_version is not None:
            return last_version.date
        return None


@admin.register(RefbooksVersions)
class RefbooksVersionsBAdmin(admin.ModelAdmin):
    list_display = [
        "CodeRefbook",
        "NameRefbook",
        "version",
        "date",
    ]
    inlines = [
        ElementsInLine,
    ]
    search_fields = ["version", ]

    @admin.display(description="Код справочника")
    def CodeRefbook(self, obj):
        refbook = Refbooks.objects.get(pk=obj.rb_id.id)
        if refbook is not None:
            return refbook.code
        return None

    @admin.display(description="Наименование справочника")
    def NameRefbook(self, obj):
        return Refbooks.objects.get(pk=obj.rb_id.id)


admin.site.register(RefbooksElements)
