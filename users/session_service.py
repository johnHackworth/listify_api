from users.models import Session
from django.conf import settings
from crypt import crypt
from random import random


class Session_service():

    user_service = None

    def __init__(self, user_service):
        self.user_service = user_service

    def createSession(self, user_id):
        session = Session()
        session.user_id = user_id
        session.hash = crypt(str(random()), settings.SESSION_SALT) + crypt(str(random()), settings.SESSION_SALT)
        return session

    def getSession(self, request):
        if 'HTTP_USER' in request.META and 'HTTP_SESSION' in request.META and 'HTTP_HASH' in request.META:
            user_id = request.META['HTTP_USER']
            session_id = request.META['HTTP_SESSION']
            session_hash = request.META['HTTP_HASH']
            result = Session.objects.filter(user_id=user_id, id=session_id, hash=session_hash)
            if len(result) == 0:
                return None
            else:
                return result[0]
        else:
            return None

    def getLoggedUser(self, request):
        session = self.getSession(request)
        if session is not None:
            return self.user_service.findUser({"id": session.user_id})
        else:
            return None

    def logUser(self, username, password=''):
        if username is not None and password is not None:
            user = self.user_service.findUser({"login": username})
            if user is not None:
                if user.password == crypt(password, settings.PASSWORD_SALT):
                    session = self.createSession(user.id)
                    session.save()
                    return self.user_service.userSessionInfo(user, session)
        return None
