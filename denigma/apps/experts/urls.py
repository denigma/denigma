"""Experts URLs."""
from django.conf.urls.defaults import patterns


urlpatterns = patterns('experts.views',
    (r'^whoiswho', 'whoiswho'),
    (r'^$', 'index'),
)
