from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from users.handlers import LoginHandler, UserHandler
login_handler = CsrfExemptResource(LoginHandler)
user_handler = CsrfExemptResource(UserHandler)

urlpatterns = patterns('',
	url(r'^log/', login_handler),
	url(r'^(?P<identification>\w+)/$', user_handler),
	url('', user_handler),

)
