from django.db import models
from commons.models import lfyModel
from commons.exceptions import InvalidFieldsException
import json
from datetime import datetime

class User(lfyModel, models.Model):
  name = models.CharField(max_length=255, default = '')
  lastname = models.CharField(max_length=255, default = '')
  login = models.CharField(max_length=255, default = None)
  password = models.CharField(max_length=255, default = None)
  email = models.CharField(max_length=255, default = None)
  location = models.CharField(max_length=255)
  country = models.IntegerField(max_length=3, default = 1)
  gender = models.IntegerField(max_length=1, default = 1)
  birthday = models.DateField(default = "2001-01-01")
  creationdate = models.DateField(auto_now=True, auto_now_add=True)
  lastlogin = models.DateTimeField(default = str(datetime.now()))
  aboutme = models.CharField(max_length = 1024)
  languaje = models.IntegerField(max_length = 3, default = 0)
  image_id = models.IntegerField(max_length=11, default = 1)
  level = models.IntegerField(max_length=11, default = 0)
  access_number= models.IntegerField(max_length=11, default = 0, db_column="accessNumber")
  email_notifications = models.IntegerField(max_length=1, default = 0, db_column="emailNotifications")

  fields = ["id", "name", "lastname", "login", "email", "location", "country", "gender", "aboutme", "languaje", "access_number"]

  def asDict(self, fields = None):
    dictionary = super(User, self).asDict(fields)

    if self.image_id is not None and self.image_id > 0:
      imageObj = Image.objects.filter(id=self.image_id)
      if len(imageObj) > 0:
        dictionary['image_url'] = imageObj[0].url

    return dictionary

  def validate(self):
    invalidFields = []
    if self.login is None:
      invalidFields.append('login')
    if self.password is None:
      invalidFields.append('password')
    if self.email is None:
      invalidFields.append('email')
    if len(invalidFields) > 0:
      raise InvalidFieldsException(invalidFields)

class Image(models.Model):
  url = models.CharField(max_length=1024)
  user_id = models.IntegerField(max_length=11)


class Session(models.Model):
  user_id = models.IntegerField(max_length=7)
  hash = models.CharField(max_length=255)

  def asDict(self, fields = ["id", "user_id", "hash"]):
    dictionary = {}
    for field in fields:
      dictionary[field] = getattr(self,field)

    return dictionary

  def asJSON(self, fields = ["id", "user_id", "hash"]):
    return json.dumps(self.asDict(fields))


class UserList():
  fields = ["id", "name", "lastname", "login", "email", "location", "country", "gender", "aboutme", "languaje", "access_number"]

  def __init__(self, user_list, fields = None):
    self.elements = user_list
    if fields is not None:
      self.fields = fields

  def asJSON(self, fields=None):
    members = []
    if fields is None:
      fields = self.fields
    for user in self.elements:
      members.append(user.asDict(fields))
    return json.dumps(members)

  elements = []

