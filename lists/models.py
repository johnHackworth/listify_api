from django.db import models
from commons.models import lfyModel
import json
from datetime import datetime

class List(lfyModel, models.Model):
	this_moment = datetime.now()
	name = models.CharField(max_length=255)
	user_id = models.IntegerField(max_length=11)
	permissions = models.IntegerField(max_length=11)
	creation_date = models.DateTimeField(default = str(this_moment))
	description = models.TextField()
	type_id = models.IntegerField(max_length=11)