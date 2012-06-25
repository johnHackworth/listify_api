from lists.models import List
from commons.exceptions import InvalidFieldsException
from django.conf import settings
import crypt
import json

class List_service():

    item_service = None;

    def __init__(self, item_service=None):
        self.item_service = item_service

    def findOneList(self, filter):
        lists = List.objects.filter(**filter);
        if len(lists) > 0:
            return lists[0]
        else:
            return None

    def getItems(self, list):
        return self.item_service.findItems({"list_id": list.id})

    def saveList(self, lfyList):
        try:
            lfyList.validate()
        except InvalidFieldsException as invalidFields:
            raise invalidFields
        lfyList.save()
        return lfyList