from django.test import TestCase
from items.models import *

class testCaseFactory(users.tests.testCaseFactory):
	def item(self):
		item = Item()
		item.name = "Sinclair Spectrum"
		item.url = "http://spectrum.es"
		item.user_id = "1"
		item.category = 1
		item.list_id = 1
		item.item.image_url = "http://foto.jpg"
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
	casesFactory = testCaseFactory()
	
	def test_export_dictionary(self):
		item = self.casesFactory.item()
		user = self.casesFactory.user()

		itemDict = item.asDict()

		self.assertEquals(itemDict['name'], item.name)


