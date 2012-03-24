from django.db import models
from commons.models import lfyModel


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
	date = models.TimeField()
	image_id = models.IntegerField(max_length=9)
	state = models.IntegerField(max_length=11)
	screencap = models.CharField(max_length=255)

