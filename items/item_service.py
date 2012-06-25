from items.models import Item, Image, Url
from commons.exceptions import InvalidFieldsException
from django.conf import settings
import crypt
import json


class Item_service():

    list_service = None
    friendship_service = None
    user_service = None

    def __init__(self, list_service=None, friendship_service=None, user_service=None):
        self.list_service = list_service
        self.friendship_service = friendship_service
        self.user_service = user_service


    def find(self, *args, **kwargs):
        items = Item.objects.filter(**kwargs)
        if len(items) > 0:
            return items[0]
        else:
            return None


    def findOne(self, filter):
        items = Item.objects.filter(**filter)
        if len(items) > 0:
            return items[0]
        else:
            return None

    def findItems(self, filter):
        items = Item.objects.filter(**filter)
        return items

    def completeItemDict(self, item, fields):
        dictionary = item.as_dict(fields)
        if self.image_id is not None and self.image_id > 0:
            imageObj = Image.objects.filter(id=self.image_id)
            if len(imageObj) > 0:
                dictionary['image_url'] = imageObj[0].url
        if self.user_id is not None and self.user_id > 0:
            user = self.user_service.findUser({"id": self.user_id})
            dictionary['user'] = user.as_dict(["name", "lastname", "id", "login"])
        if self.list_service is not None:
            containerList = self.list_service.findOneList({"id": item.list_id})
            dictionary["list"] = containerList.as_dict()
        return dictionary

    def saveItem(self, item):
        try:
            item.validate()
        except InvalidFieldsException as invalidFields:
            raise invalidFields
        item.save()
        return item

    def is_viewable(self, article, user_id):
        if self.list_service is not None:
            container_list = self.list_service.findOneList({"id": article.list_id})

            relation_level = self.friendship_service.getRelationById(user_id, article.user_id)
            if relation_level >= container_list.permissions:
                return True

        return False


