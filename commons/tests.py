from django.test import TestCase
from users.models import *
from users.session_service import *
from commons.models import lfyHandler
from commons.mocks import RequestFactory


class lfyHandlerTests(TestCase):
    def test_getRequestData(self):
        handler = lfyHandler()
        rf = RequestFactory()
        request = rf.get('fake/path')
        request = rf.setHeaders(1, 2, 3, request)

        requestData = handler.getSessionData(request)

        self.assertTrue('user_id' in requestData)
        self.assertTrue('session_id' in requestData)
        self.assertTrue('session_hash' in requestData)
        self.assertEquals(requestData['user_id'], 1)
        self.assertEquals(requestData['session_id'], 2)
        self.assertEquals(requestData['session_hash'], 3)
