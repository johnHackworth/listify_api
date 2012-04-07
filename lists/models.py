from django.db import models
from commons.models import lfyModel
from commons.exceptions import InvalidFieldsException
import json
from datetime import datetime

class List(lfyModel, models.Model):

	name = models.CharField(max_length=255, default=None)
	user_id = models.IntegerField(max_length=11)
	permissions = models.IntegerField(max_length=11, default = 0)
	creation_date = models.DateTimeField(default = str(datetime.now()))
	description = models.TextField()
	type_id = models.IntegerField(max_length=11, default = 0)

	fields = ["name", "user_id", "permissions", "creation_date", "description", "id"]

	def validate(self):
		invalidFields = []
		if self.user_id is None:
			invalidFields.append('user_id')
		if self.name is None:
			invalidFields.append('name')
		if len(invalidFields) > 0:
			raise InvalidFieldsException(invalidFields)
