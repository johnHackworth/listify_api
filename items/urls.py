from django.conf.urls.defaults import patterns, include, url
from commons.models import CsrfExemptResource
from items.handlers import ItemHandler
 

item_handler = CsrfExemptResource(ItemHandler)

urlpatterns = patterns('',
	url(r'^(?P<id>\w+)/$', item_handler),
	url('', item_handler),
)
