from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from items.models import Item
from items.item_service import Item_service
from users.session_service import Session_service
from users.user_service import User_service
from commons.exceptions import InvalidFieldsException
from commons.models import lfyHandler


class ItemHandler(lfyHandler):
    allowed_methods = ('GET, PUT, POST, DELETE')
    item_service = Item_service(None)
    user_service = User_service()
    session_service = Session_service(user_service)

    fields = ["name", "url", "image_url", "text", "price", "currency", "author", "state", "screencap", "list_id"]

    def read(self, request, id):
        item = self.item_service.findOne({"id": id})
        if item is not None:
            loggedUser = self.session_service.getLoggedUser(request)
            ownerUser = self.user_service.findUser({"id": item.user_id})
            # @TODO : waiting for list_service to be implemented
            # if self.list_service.getPermissions(item.list_id) <= self.user_service.getRelationLevel(ownerUser, loggedUser):
            if True:
                return HttpResponse(item.as_json())
            else:
                return HttpResponseNotAllowed('<h1>not allowed</h1>')
        else:
            return HttpResponseNotFound()

    def update(self, request, id):
        loggedUser = self.session_service.getLoggedUser(request)
        if loggedUser is not None:
            item = self.item_service.findOne({"id": id})
            if item is not None:
                if loggedUser.id != item.user_id:
                    return HttpResponseForbidden('<h1>not the owner</h1>')
                else:
                    self.fromRequest(request, item, self.fields)
                    self.item_service.saveItem(item)

                return HttpResponse(item.as_json())
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')

    def delete(self, request, id):
        loggedUser = self.session_service.getLoggedUser(request)

        if loggedUser is not None:
            item = self.item_service.findOne({"id": id})
            if item is not None:
                if loggedUser.id != item.user_id:
                    return HttpResponseForbidden('<h1>not the owner</h1>')
                else:
                    item.delete()
                    return HttpResponse('<h1>ok</h1>')
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')

    def create(self, request):

        loggedUser = self.session_service.getLoggedUser(request)
        if loggedUser is not None:
            item = Item()
            self.fromRequest(request, item, self.fields)
            item.user_id = loggedUser.id

            try:
                item.validate()
            except InvalidFieldsException as invalidFields:
                return HttpResponseForbidden(invalidFields)

            self.item_service.saveItem(item)

            return HttpResponse(item.as_json())
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')
