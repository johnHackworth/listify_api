from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	
	url(r'^(?P<user_id>\d+)/$', 'users.views.getUserById'),
	url(r'^(?P<login>\w+)/$', 'users.views.getUserByLogin'),
)
