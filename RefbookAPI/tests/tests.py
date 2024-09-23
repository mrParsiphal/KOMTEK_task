from django.test import TestCase

from api_v1.models import Refbooks, RefbooksVersions, RefbooksElements


class YourTestClass(TestCase):

    def setUp(self):
        print("Запуск тестов.")
        # Создание справочников
        Refbooks.objects.create(code="1", name="Справочник №1", description="Описание №1") #id=1
        Refbooks.objects.create(code="2", name="Справочник №2", description="Описание №2") #id=2
        Refbooks.objects.create(code="3", name="Справочник №3", description="Описание №3") #id=3
        # Создание версий справочника №1
        RefbooksVersions.objects.create(version="0.1.0", date="2024-09-08", rb_id_id=1) #id=1
        RefbooksVersions.objects.create(version="0.1.1", date="2024-09-09", rb_id_id=1) #id=2
        RefbooksVersions.objects.create(version="0.1.2", date="2024-09-10", rb_id_id=1) #id=3
        # Создание версий справочника №2
        RefbooksVersions.objects.create(version="0.1", date="2024-09-08", rb_id_id=2) #id=4
        RefbooksVersions.objects.create(version="0.2", date="2024-09-10", rb_id_id=2) #id=5
        RefbooksVersions.objects.create(version="0.3", date="2024-09-12", rb_id_id=2) #id=6
        # Создание создание элементов версии №0.1 справочника №1
        RefbooksElements.objects.create(code="1", value="1", rbv_id_id=3) #id=1
        RefbooksElements.objects.create(code="2", value="2", rbv_id_id=3) #id=2
        # Создание создание элементов версии №0.1 справочника №2
        RefbooksElements.objects.create(code="3", value="3", rbv_id_id=5) #id=3
        RefbooksElements.objects.create(code="4", value="4", rbv_id_id=5) #id=4

    def tearDown(self):
        pass

    def test_GetRebooks_without_date(self):
        # Проверка вывода всех справочников.
        resp = self.client.get(path="/refbooks?format=json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue({
            "refbooks": [
                {
                    "id": 1,
                    "code": "1",
                    "name": "Справочник №1"
                },
                {
                    "id": 2,
                    "code": "2",
                    "name": "Справочник №2"
                },
                {
                    "id": 3,
                    "code": "3",
                    "name": "Справочник №3"
                }
            ]
        } == resp.json())

    def test_GetRebook_with_date_1(self):
        # Проверка вывода всех справочников по дате.
        resp = self.client.get(path="/refbooks?format=json&date=2024-09-12")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue({"refbooks": [
            {
                "id": 2,
                "code": "2",
                "name": "Справочник №2"
            }
        ]} == resp.json())

    def test_GetRebook_with_date_2(self):
        # Проверка на отработку исключения при указании слишком поздней даты.
        resp = self.client.get(path="/refbooks?format=json&date=2024-10-01")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json() == {"error": "Версии справочников подходящие запросу отсутствуют."})

    def test_GetRebookElements_without_version(self):
        # Проверка вывода значений актуальной версии.
        resp = self.client.get(path="/refbooks/1/elements?format=json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue({"elements": [
            {
                "code": "1",
                "value": "1"
            },
            {
                "code": "2",
                "value": "2"
            },
        ]} == resp.json())

    def test_GetRebookElements_with_version_1(self):
        # Проверка вывода значений указанной версии.
        resp = self.client.get(path="/refbooks/1/elements?format=json&version=0.1.2")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue({"elements": [
            {
                "code": "1",
                "value": "1"
            },
            {
                "code": "2",
                "value": "2"
            },
        ]} == resp.json())

    def test_GetRebookElements_with_version_2(self):
        # Проверка на отработку исключения отсутствия элементов.
        resp = self.client.get(path="/refbooks/2/elements?format=json&version=0.3")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json() == {"error": "Елементы подходящие запросу отсутствуют."})

    def test_methods_FindRebookVersion_1(self):
        # Проверка на отработку исключения отсутствия справочника.
        resp = self.client.get(path="/refbooks/10/elements?format=json")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json() == {"error": "Указанный справочник отсутствует или не имеет версий!"})

    def test_methods_FindRebookVersion_2(self):
        # Проверка на отработку исключения отсутствия версий.
        resp = self.client.get(path="/refbooks/3/elements?format=json")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json() == {"error": "Указанный справочник отсутствует или не имеет версий!"})

    def test_methods_FindRebookVersion_3(self):
        # Проверка на отработку исключения отсутствия указанной версии.
        resp = self.client.get(path="/refbooks/3/elements?format=json&version=0.1")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json() == {"error": "Данная версия справочника не найдена."})

    def test_RebookCheckElement_1(self):
        # Проверка присутствия элемента в справочнике.
        resp = self.client.get(path="/refbooks/1/check_element?format=json&code=1&value=1")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.content == b'true')

    def test_RebookCheckElement_2(self):
        # Проверка отсутствия элемента в справочнике.
        resp = self.client.get(path="/refbooks/1/check_element?format=json&code=3&value=3")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.content == b'false')
