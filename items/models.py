from django.db import models
from commons.models import lfyModel
from datetime import datetime

class Item(lfyModel, models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	user_id = models.IntegerField(max_length=11)
	category = models.IntegerField(max_length=5)
	list_id = models.IntegerField(max_length=9)
	image_url = models.CharField(max_length=255)
	text = models.CharField(max_length=1024)
	price = models.FloatField(max_length=255)
	currency = models.IntegerField(max_length=3)
	author = models.CharField(max_length=255)
	date = models.DateTimeField(str(datetime.now()))
	image_id = models.IntegerField(max_length=9)
	state = models.IntegerField(max_length=11)
	screencap = models.CharField(max_length=255)

	fields = ["name", "url", "image_url", "text", "price", 
	"currency", "author", "date", "state", "screencap"]

class Image(lfyModel, models.Model):
	url = models.CharField(max_length=255)
	url_id = models.IntegerField(max_length=11)
	user_id = models.IntegerField(max_length=11)
	item_id = models.IntegerField(max_length=11)

class Url(lfyModel, models.Model):
	urlExt = models.CharField(max_length=1024)
	urlInt = models.CharField(max_length=1024)
	online = models.BooleanField(default = False)