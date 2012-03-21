from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from users.handlers import LoginHandler, UserHandler
 
login_handler = Resource(LoginHandler)
user_handler = Resource(UserHandler)

urlpatterns = patterns('',
	url(r'^log/', login_handler),
	url(r'^(?P<identification>\w+)/$', user_handler),
)
