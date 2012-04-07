from django.db import models
from commons.models import lfyModel
from commons.exceptions import InvalidFieldsException
from datetime import datetime

class Item(lfyModel, models.Model):
	name = models.CharField(max_length=255, default=None)
	url = models.CharField(max_length=255, default=None)
	user_id = models.IntegerField(max_length=11)
	category = models.IntegerField(max_length=5, default = 0)
	list_id = models.IntegerField(max_length=9)
	image_url = models.CharField(max_length=255)
	text = models.CharField(max_length=1024)
	price = models.FloatField(max_length=255, default = 0)
	currency = models.IntegerField(max_length=3, default = 0)
	author = models.CharField(max_length=255)
	date = models.DateTimeField(default = str(datetime.now()))
	image_id = models.IntegerField(max_length=9, default=1)
	state = models.IntegerField(max_length=11, default =0)
	screencap = models.CharField(max_length=255)

	fields = ["name", "url", "image_url", "text", "price", 
	"currency", "author", "date", "state", "screencap", "id"]

	def validate(self):
		invalidFields = []
		if self.user_id is None:
			invalidFields.append('user_id')
		if self.list_id is None:
			invalidFields.append('list_id')
		if self.name is None:
			invalidFields.append('name')
		if self.url is None:
			invalidFields.append('url')
		if len(invalidFields) > 0:
			raise InvalidFieldsException(invalidFields)

class Image(lfyModel, models.Model):
	url = models.CharField(max_length=255)
	url_id = models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	item_id = models.IntegerField(max_length=11)

class Url(lfyModel, models.Model):
	urlExt = models.CharField(max_length=1024)
	urlInt = models.CharField(max_length=1024)
	online = models.BooleanField(default = False)