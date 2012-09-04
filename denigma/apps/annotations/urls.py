# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('annotations.views',
                      url(r'^add_data', 'add_data'),
                      url(r'^$', 'index'),
)
