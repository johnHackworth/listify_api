from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from users.user_service import User_service
from piston.handler import BaseHandler
 
class LoginHandler(BaseHandler):
  allowed_methods = ('GET')
  user_service = User_service();
 
  def read(self, request):

	login = request.GET.get('username')
	password = request.GET.get('password')
	result = self.user_service.logUser(login, password)
	if result is None:
		return HttpResponseNotFound('<h1>Login or password incorrect</h1>')
	else:
		return HttpResponse(result)
