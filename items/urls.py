from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from items.handlers import ItemHandler
 
item_handler = Resource(ItemHandler)

urlpatterns = patterns('',
	url(r'^(?P<id>\w+)/$', item_handler),
)
