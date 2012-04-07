from django.conf.urls.defaults import patterns, include, url
from commons.models import CsrfExemptResource
from lists.handlers import ListHandler
 
list_handler = CsrfExemptResource(ListHandler)

urlpatterns = patterns('',
	url(r'^(?P<id>\w+)/$', list_handler),
	url('', list_handler),
)
