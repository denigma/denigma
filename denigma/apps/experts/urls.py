"""Experts URLs."""
from django.conf.urls import patterns, url

from views import ProfileList, CreateProfile, UpdateProfile


urlpatterns = patterns('experts.views',
    url(r'^whoiswho', 'whoiswho'),
    url(r'^$', ProfileList.as_view(), name='experts'),
    url(r'^archive', 'index', name="experts-archive"),
    url(r'^create/$', CreateProfile.as_view(), name='create-expert-profile'),
    url(r'^update/(?P<pk>\d+)', UpdateProfile.as_view(), name='update-expert-profile'),
    url(r'^(?P<expertname>.+)/$', 'detail'),
)
