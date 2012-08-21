"""Users urls."""
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^whoiswho', 'whoiswho'),
    (r'^list', 'list'),
    (r'^$', views.list)
)
