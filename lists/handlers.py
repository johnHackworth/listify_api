from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from lists.models import List
from lists.list_service import List_service
from users.user_service import User_service
from users.session_service import Session_service
from commons.exceptions import MethodNotAllowedException, InvalidFieldsException
from commons.models import lfyHandler


 
class ListHandler(lfyHandler):
  allowed_methods = ('GET, PUT, POST, DELETE')
  user_service = User_service()
  list_service = List_service(user_service)
  session_service = Session_service(user_service)

  fields = ["name", "permissions", "description"]
 
  def read(self, request, id):
    lfyList = self.list_service.findOneList({"id":id})
    if lfyList is not None:
      loggedUser = self.session_service.getLoggedUser(request)
      ownerUser = self.user_service.findUser({"id":lfyList.user_id})
      # @TODO: test if the users are friends against teh
      if True:
        return HttpResponse(lfyList.asJSON())
      else:
        return HttpResponseNotAllowed('<h1>not allowed</h1>')
    else:
      return HttpResponseNotFound()

  def update(self, request, id):
    loggedUser = self.session_service.getLoggedUser(request)
    if loggedUser is not None:
      lfyList = self.list_service.findOneList({"id":id})
      if list is not None:
        if loggedUser.id != lfyList.user_id:
          return HttpResponseForbidden('<h1>not the owner</h1>')
        else:
          self.fromRequest(request, lfyList, self.fields)
          self.list_service.saveList(lfyList)
        
        return HttpResponse(lfyList.asJSON())
      else:
        return HttpResponseNotFound()      
    else:
      return HttpResponseForbidden('<h1>not a user</h1>')      

  def delete(self, request, id):
    loggedUser = self.session_service.getLoggedUser(request)
    
    if loggedUser is not None:
      lfyList = self.list_service.findOneList({"id":id})
      if lfyList is not None:
        if loggedUser.id != lfyList.user_id:
          return HttpResponseForbidden('<h1>not the owner</h1>')
        else:
          lfyList.delete()
          return HttpResponse('<h1>ok</h1>')
      else:
        return HttpResponseNotFound()      

    else:
      return HttpResponseForbidden('<h1>not a user</h1>')      

  def create(self, request):

    loggedUser = self.session_service.getLoggedUser(request)
    if loggedUser is not None:
      lfyList = List()
      self.fromRequest(request, lfyList, self.fields)
      lfyList.user_id = loggedUser.id

      try:
        self.list_service.saveList(lfyList)
      except InvalidFieldsException as invalidFields:
        return HttpResponseForbidden(invalidFields)

      return HttpResponse(lfyList.asJSON())
    else:
      return HttpResponseForbidden('<h1>not a user</h1>')      