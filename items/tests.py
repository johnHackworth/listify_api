from django.test import TestCase
from items.models import *
from items.item_service import *
from commons.exceptions import InvalidFieldsException
from items.mocks import ItemTestCaseFactory


class ItemModelTest(TestCase):
    cases_factory = ItemTestCaseFactory()

    def test_export_dictionary(self):
        item = self.cases_factory.item()

        itemDict = item.as_dict()
        self.assertEquals(itemDict['name'], item.name)
        self.assertFalse("image" in itemDict)


class ItemServiceTest(TestCase):
    cases_factory = ItemTestCaseFactory()
    item_service = Item_service(None)

    def test_findOneItem(self):
        item = self.cases_factory.item()
        item.save()
        item = self.item_service.findOneItem({"text": "old computer"})
        self.assertEquals(item.name, "Sinclair Spectrum")

    def test_findItems(self):
        item = self.cases_factory.item()
        item2 = self.cases_factory.item()
        item.save()
        item2.save()

        items = self.item_service.findItems({"name": "Sinclair Spectrum"})
        self.assertEquals(len(items), 2)
        self.assertEquals(items[0].name, items[1].name)
        self.assertTrue(items[0].url == "http://spectrum.es")

    def test_saveItem(self):
        it = Item()
        success = False
        try:
            self.item_service.saveItem(it)
        except InvalidFieldsException:
            success = True
        except:
            success = False

        self.assertTrue(success)

        it.list_id = 1
        success = False
        try:
            self.item_service.saveItem(it)
        except InvalidFieldsException:
            success = True
        except:
            success = False
        self.assertTrue(success)

        it.name = 'prueba'
        success = False
        try:
            self.item_service.saveItem(it)
        except InvalidFieldsException:
            success = True
        except:
            success = False
        self.assertTrue(success)

        it.user_id = 1
        success = False
        try:
            self.item_service.saveItem(it)
        except InvalidFieldsException:
            success = True
        except:
            success = False
        self.assertTrue(success)

        it.url = 'url'
        success = False
        try:
            self.item_service.saveItem(it)
            success = True
        except Exception as e:
            print e
            success = False
        self.assertTrue(success)



