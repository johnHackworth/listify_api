from django.contrib.auth.models import User
from users.services import User_service
from piston.handler import BaseHandler
 
class LoginHandler(BaseHandler):
  allowed_methods = ('GET')
  user_service = User_service();
 
  def read(self, request):
		login = request.GET('username')
		password = request.GET('password')

		return user_service.logUser(login, password)