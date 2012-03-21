from users.models import User
from django.conf import settings
import crypt

class User_service():

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
					return "create a session goes here"
		return None


		