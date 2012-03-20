from django.db import models
import json

class User(models.Model):
  id = models.IntegerField(max_length=7)    
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  login = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  country = models.IntegerField(max_length=3)
  gender = models.IntegerField(max_length=1)
  birthday = models.DateField()
  creationdate = models.DateField(auto_now=True, auto_now_add=True)
  lastlogin = models.DateField()
  aboutme = models.CharField(max_length=1024)
  languaje = models.IntegerField(max_length=3)
  image_id = models.IntegerField(max_length=11)
  level = models.IntegerField(max_length=11)
  access_number= models.IntegerField(max_length=11, db_column="accessNumber")
  email_notifications = models.IntegerField(max_length=1, db_column="emailNotifications")
  
  def asJSON(self):
    fields = ["id", "name", "lastname", "login", "email", "location", "country", "gender", "birthday", "aboutme", "languaje", "access_number"]
    jsonObj = {}
    for field in fields:
      jsonObj[field] = getattr(self,field)

    if self.image_id is not None and self.image_id > 0:
      imageObj = Image.objects.filter(id=self.image_id)
      if len(imageObj) > 0:
        jsonObj['image_url'] = imageObj[0].url

    return  json.dumps(jsonObj)


class Image(models.Model):
  id = models.IntegerField(max_length=11)   
  url = models.CharField(max_length=1024)
  user_id = models.IntegerField(max_length=11)