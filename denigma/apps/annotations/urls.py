# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('annotations.views',
    url(r'^bulk_upload', 'bulk_upload'),
    #url(r'^bulk_upload/data', 'bulk_upload_data'),
    url(r'^species', 'species', name='species'),
    url(r'^tissues/$', 'tissues', name='tissues'),
    url(r'^tissues/(?P<pk>[\d]+)$', 'tissue'),
    url(r'^$', 'index', name='annotations'),
)

