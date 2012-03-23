from users.models import User, Session
from users.session_service import *
from django.conf import settings
import crypt
import json

class User_service():

	sessionService = Session_service()

	def findUser(self, filter):
		users = User.objects.filter(**filter);
		if len(users) > 0:
			return users[0]
		else:
			return None

	def logUser(self, username, password = ''):
		if username is not None and password is not None:
			user = self.findUser({"login":username});
			if user is not None:
				if user.password == crypt.crypt(password, settings.PASSWORD_SALT):
					session = self.sessionService.createSession(user.id)
					session.save()
					return self.userSessionInfo(user, session)
		return None

	def userSessionInfo(self, user, session):
		userDict = user.asDict()
		userDict['session'] = session.asDict(["id", "hash"])
		return json.dumps(userDict)





		