"""Experts URLs."""
from django.conf.urls.defaults import patterns


urlpatterns = patterns('experts.views',
    (r'^whoiswho', 'whoiswho'),
    (r'^$', 'index'),
    (r'^(?P<expertname>[a-zA-Z_]+)/$', 'detail'),
)
