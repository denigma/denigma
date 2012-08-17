# -*- coding: utf-8 -*-
"""Urls for news."""
from django.conf.urls.defaults import *

from d.annotations.views import find


urlpatterns = patterns('',
                       (r'^$', find),)
