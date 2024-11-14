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
        return RefbooksVersions.objects.filter(rb_id=obj.pk).latest("date").date


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
        return obj.rb_id.code

    @admin.display(description="Наименование справочника")
    def NameRefbook(self, obj):
        return obj.rb_id


@admin.register(RefbooksElements)
class RefbooksElementsBAdmin(admin.ModelAdmin):
    list_display = [
        "VersionRefbook",
        "code",
        "value",
    ]
    search_fields = ["code", ]

    @admin.display(description="Версия справочника")
    def VersionRefbook(self, obj):
        return obj.rbv_id
