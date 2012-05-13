from django.conf.urls.defaults import patterns, include, url
import users.urls
import items.urls
import lists.urls
import friends.urls
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'listify_api.views.home', name='home'),
    # url(r'^listify_api/', include('listify_api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^user/', include(users.urls)),
   	url(r'^item/', include(items.urls)),
   	url(r'^list/', include(lists.urls)),
    url(r'^friends/', include(friends.urls)),
    url(r'^doc/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/var/listify_api/build/html/'}),
)
