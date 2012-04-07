from items.models import Item, Image, Url
from commons.exceptions import InvalidFieldsException
from django.conf import settings
import crypt 
import json

class Item_service():

	list_service = None;

	def __init__(self, list_service):
		self.list_service = list_service

	def findOneItem(self, filter):
		items = Item.objects.filter(**filter);
		if len(items) > 0:
			return items[0]
		else:
			return None

	def findItems(self, filter):
		items = Item.objects.filter(**filter);
		return items

	def completeItemDict(self, item, fields):
		dictionary = item.asDict(fields)
		if self.image_id is not None and self.image_id > 0:
			imageObj = Image.objects.filter(id=self.image_id)
    		if len(imageObj) > 0:
				dictionary['image_url'] = imageObj[0].url
		if self.user_id is not None and self.user_id > 0:
			user = user_service.findUser({"id":self.user_id})
			dictionary['user'] = user.asDict(["name","lastname","id","login"])
		if self.list_service is not None and self.list_id is not None and self.user_list > 0:
		 	containerList = list_service.findList({"id": self.id})
		 	dictionary["list"] = containerList.asDict()
		return dictionary
	def saveItem(self, item):
		try:
			item.validate()
		except InvalidFieldsException as invalidFields:
			raise invalidFields
		item.save()
		return item
