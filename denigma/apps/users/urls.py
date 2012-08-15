"""Users urls."""
from django.conf.urls.defaults import *


urlpatterns = patterns('users.views',
    (r'^whoiswho', 'whoiswho'),
    (r'^list', 'list'),
    (r'^', 'list')
)
