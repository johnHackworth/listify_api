from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from users.user_service import User_service
from users.session_service import Session_service
from piston.handler import BaseHandler
 
class LoginHandler(BaseHandler):
  allowed_methods = ('GET')
  user_service = User_service()
  session_service = Session_service(user_service)
 
  def read(self, request):

	login = request.GET.get('username')
	password = request.GET.get('password')
	result = self.session_service.logUser(login, password)
	if result is None:
		return HttpResponseNotFound('<h1>Login or password incorrect</h1>')
	else:
		return HttpResponse(result)

	def delete(self, id, request):
		pass

class UserHandler(BaseHandler):

	allowed_methods = ('GET')
  	user_service = User_service();	
  	
	def getUser(self, value, field):
		user = self.user_service.findUser({field: value})
		if user is not None:
			return HttpResponse(user.asJSON())
  		else:
  			return HttpResponseNotFound('<h1>User not found</h1>')

  	def read(self, request, identification):
  		if identification.isdigit():
  			return self.getUser(identification,"id")
  		else:
  			return self.getUser(identification,"login")