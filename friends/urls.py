# -*- coding: utf-8 -*-
"""
    listify_api.friends.urls
    ~~~~~~~~~~~~~~~~~~~

    Entry points for friendship related operations

"""
from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from friends.handlers import FriendshipHandler

friends_handler = CsrfExemptResource(FriendshipHandler)

urlpatterns = patterns('',
  url(r'^(?P<user_id>\w+)/(?P<friend_id>\w+)/$', friends_handler),
)
