from django.http import HttpResponse, HttpResponseNotFound
from users.models import User
from users.user_service import User_service

manager = User_service()

def getUser(value, field):
  user = manager.findUser({field: value})
  if user is not None:
    return HttpResponse(user.asJSON())
  else:
    return HttpResponseNotFound('<h1>User not found</h1>')

def getUserById(self, user_id):
  return getUser(user_id,"id")

def getUserByLogin(self, login):
  return getUser(login,"login")