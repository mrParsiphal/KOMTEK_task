from django.db import models

class Refbooks(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Refbooks"
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class RefbooksVersions(models.Model):
    version = models.CharField(max_length=50, verbose_name="Версия")
    date = models.DateField(verbose_name="Дата")
    rb_id = models.ForeignKey(Refbooks, on_delete=models.CASCADE, verbose_name="Справочник")

    def __str__(self):
        return self.version

    class Meta:
        db_table = "RefbooksVersions"
        unique_together = [["version", "rb_id"], ["rb_id", "date"]]
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"


class RefbooksElements(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    value = models.CharField(max_length=300, verbose_name="Значение")
    rbv_id = models.ForeignKey(RefbooksVersions, on_delete=models.CASCADE, verbose_name="Версия справочника")

    def __str__(self):
        return f"Элемент справочника {self.code}"

    class Meta:
        db_table = "RefbooksElements"
        unique_together = [["code", "rbv_id"]]
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
