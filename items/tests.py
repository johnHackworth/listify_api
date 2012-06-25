from django.test import TestCase
from items.models import *
from items.item_service import *
from lists.models import *
from commons.exceptions import InvalidFieldsException
from items.mocks import ItemTestCaseFactory
from django.utils.unittest import skipIf
from friends.mocks import Frienship_service_mock
from lists.mocks import List_service_mock


class ItemModelTest(TestCase):
    cases_factory = ItemTestCaseFactory()

    def test_export_dictionary(self):
        item = self.cases_factory.item()

        itemDict = item.as_dict()
        self.assertEquals(itemDict['name'], item.name)
        self.assertFalse("image" in itemDict)


class ItemServiceTest(TestCase):
    cases_factory = ItemTestCaseFactory()
    list_service_mock = List_service_mock()
    friendship_service_mock = Frienship_service_mock()
    item_service = Item_service(list_service_mock, friendship_service_mock)

    def test_findOne(self):
        item = self.cases_factory.item()
        item.save()
        item = self.item_service.findOne({"text": "old computer"})
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

    def test_is_viewable(self):
        #@todo: we should mock List here
        it = self.cases_factory.item()
        test_list = List(user_id=10, name="test", permissions=0)
        test_list.save()
        self.list_service_mock.list = test_list

        it.list_id = test_list.id
        it.save()

        viewable = self.item_service.is_viewable(it, 1)
        self.assertTrue(viewable)

    def test_is_not_viewable(self):
        it = self.cases_factory.item()
        test_list = List(user_id=10, name="test", permissions=2)
        test_list.save()
        self.list_service_mock.list = test_list

        it.list_id = test_list.id
        it.save()

        viewable = self.item_service.is_viewable(it, 1)
        self.assertFalse(viewable)





