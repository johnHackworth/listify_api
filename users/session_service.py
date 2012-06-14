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

    def getSession(self, user_id, session_id, session_hash):
        result = Session.objects.filter(user_id=user_id, id=session_id, hash=session_hash)
        if len(result) == 0:
            return None
        else:
            return result[0]

    def deleteSession(self, session_id, session_hash):
        current_session = Session.objects.filter(id=session_id, hash=session_hash)
        current_session.delete()
        return None

    def getLoggedUser(self, sessionDTO):
        session = self.getSession(sessionDTO["user_id"], sessionDTO["session_id"], sessionDTO["session_hash"])
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
