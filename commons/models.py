from datetime import datetime
from piston.resource import Resource
from piston.handler import BaseHandler
from commons.exceptions import MethodNotAllowedException
import json


class lfyModel():
    fields = []

    def asDict(self, fields=None):
        if fields is None:
            fields = self.fields
        dictionary = {}
        for field in fields:
            fieldValue = getattr(self, field)
            if type(fieldValue) is datetime:
                fieldValue = unicode(fieldValue)

            dictionary[field] = fieldValue
        return dictionary

    def asJSON(self, fields=None):
        return json.dumps(self.asDict(fields))


class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)


class lfyHandler(BaseHandler):

    def fromRequest(self, request, entity, fields):
        for field in fields:
            fieldVal = None
            if request.META['REQUEST_METHOD'] == 'POST':
                if field is not 'id' and field in request.POST:
                    fieldVal = request.POST.get(field)
            elif field is not 'id' and request.META['REQUEST_METHOD'] == 'PUT':
                if field in request.PUT:
                    fieldVal = request.PUT.get(field)
            else:
                raise MethodNotAllowedException(request.META['REQUEST_METHOD'])
            if fieldVal is not None:
                setattr(entity, field, fieldVal)

    def getSessionData(self, request):
        dictionary = {}
        if 'HTTP_USER' in request.META and 'HTTP_SESSION' in request.META and 'HTTP_HASH' in request.META:
            dictionary['user_id'] = request.META['HTTP_USER']
            dictionary['session_id'] = request.META['HTTP_SESSION']
            dictionary['session_hash'] = request.META['HTTP_HASH']
        return dictionary
