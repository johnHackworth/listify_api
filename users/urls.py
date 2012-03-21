from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from users.handlers import LoginHandler
 
login_handler = Resource(LoginHandler)

urlpatterns = patterns('',
	url(r'^log/', login_handler),
	url(r'^(?P<user_id>\d+)/$', 'users.views.getUserById'),
	url(r'^(?P<login>\w+)/$', 'users.views.getUserByLogin'),
    
)
