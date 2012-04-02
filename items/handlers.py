from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from items.item_service import Item_service
from users.session_service import Session_service
from users.user_service import User_service
from piston.handler import BaseHandler
 
class ItemHandler(BaseHandler):
  allowed_methods = ('GET, PUT, POST, DELETE')
  item_service = Item_service(None)
  user_service = User_service()
  session_service = Session_service(user_service)
 
  def read(self, request, id):
    loggedUser = self.session_service.getLoggedUser(request)
    
    if loggedUser is not None:
      item = self.item_service.findOneItem({"id":id})
      return HttpResponse(item.asJSON())
    else:
      return HttpResponseForbidden('<h1>not a user</h1>')

  def update(self, request, id):
  	loggedUser = self.session_service.getLoggedUser(request)
    loggedUser = True
    if loggedUser is not None:
      item = self.item_service.findOneItem({"id":id})
      dictionary = self.fromRequest(request, item)
      self.item_service.saveItem(item)
      
      return HttpResponse(item.asJSON())
    else:
      return HttpResponseForbidden('<h1>not a user</h1>')


  def save(self):
  	pass
  def create(self):
  	pass

  def fromRequest(self, request, item):
    fields = ["name", "url", "image_url", "text", "price", "currency", "author", "date", "state", "screencap"]
    dictionary = {}

    for field in fields:
      setattr(item,field, request.PUT.get(field))