# -*- coding: utf-8 -*-
"""Urls for news."""
from django.conf.urls.defaults import *

from links.views import links_by_language


urlpatterns = patterns('',
                       url(r'^$', links_by_language, name='links_list'),
                       )
