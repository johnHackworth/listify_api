from django.test import TestCase
from items.models import *
from items.item_service import *
from users.tests import usersTestCaseFactory

class itemTestCaseFactory(usersTestCaseFactory):
	def item(self):
		item = Item()
		item.name = "Sinclair Spectrum"
		item.url = "http://spectrum.es"
		item.user_id = "1"
		item.category = 1
		item.list_id = 1
		item.image_url = "http://foto.jpg"
		item.text = "old computer"
		item.price = 10.5
		item.currency = 1
		item.author = ""
		item.date = "2001-01-01"
		item.image_id = 1
		item.state = 1
		item.screencap = ""
		return item


class ItemModelTest(TestCase):
	casesFactory = itemTestCaseFactory()
	
	def test_export_dictionary(self):
		item = self.casesFactory.item()
		user = self.casesFactory.user()

		itemDict = item.asDict()
		self.assertEquals(itemDict['name'], item.name)
		self.assertFalse("image" in itemDict)

class ItemServiceTest(TestCase):
	cases_factory = itemTestCaseFactory()
	item_service = Item_service()

	def test_get_item(self):
		it1 = self.cases_factory.item().save()

		item = self.item_service.findOneItem({"text":"old computer"})

		self.assertEquals(item.name, "Sinclair Spectrum")

	def test_find_items(self):
		it1 = self.cases_factory.item().save()
		it2 = self.cases_factory.item().save()

		items = self.item_service.findItems({"name":"Sinclair Spectrum"})

		self.assertEquals(len(items), 2)
		self.assertEquals(items[0].name, items[1].name)
		self.assertTrue(items[0].url == "http://spectrum.es")

		

