from users.models import User

class User_service():
	def findUser(self, filter):
		users = User.objects.filter(filter);
		if len(users) > 0:
			return users[0]
		else:
			return None