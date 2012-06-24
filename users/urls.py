from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from users.handlers import SessionHandler, UserHandler, FriendsHandler, PasswordChangeHandler
session_handler = CsrfExemptResource(SessionHandler)
password_change_handler = CsrfExemptResource(PasswordChangeHandler)
user_handler = CsrfExemptResource(UserHandler)
friends_handler = CsrfExemptResource(FriendsHandler)

urlpatterns = patterns('',
    url(r'^session/', session_handler),
    url(r'^passwordChange/', password_change_handler),
    url(r'^(?P<identification>\w+)/friends/$', friends_handler),
    url(r'^(?P<identification>\w+)/$', user_handler),
    url('', user_handler),

)
