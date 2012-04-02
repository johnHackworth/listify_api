from users.models import User, Session
from users.session_service import *
from django.conf import settings
import crypt
import json

class User_service():

	session_service = None

	def __init(self, session_service):
		self.session_service = session_service

	def findUser(self, filter):
		users = User.objects.filter(**filter);
		if len(users) > 0:
			return users[0]
		else:
			return None

	def userSessionInfo(self, user, session):
		userDict = user.asDict()
		userDict['session'] = session.asDict(["id", "hash"])
		return json.dumps(userDict)





		