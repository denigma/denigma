"""Dataset urls."""
from django.conf.urls.defaults import *


urlpatterns = patterns('datasets.views',
    (r'^references/update', 'update'),
    (r'^references/', 'show_all'),
    (r'^genage/describe', 'describe'),
    (r'^genage/functional_description', 'functional_description'),
    (r'^genage/integrity', 'integrity'),
    (r'^(?P<table>\w+)/replace/(?P<field>\w+)/(?P<term>.+)/(?P<by>.+)/$', 'replace'), #
                       #
    (r'^gendr/dump', 'dump'),
)
