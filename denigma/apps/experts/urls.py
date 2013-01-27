"""Experts URLs."""
from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from utils.ajax import HybridDetailView

from views import ProfileList, CreateProfile, UpdateProfile
from views import CollaborationList, CreateCollaboration, UpdateCollaboration, CollaborationView
from models import Profile, Collaboration


urlpatterns = patterns('experts.views',
    url(r'^$', 'index', name='experts'),

    # Profiles:
    url(r'^whoiswho', 'whoiswho'),
    url(r'^profiles', ProfileList.as_view(), name='experts-profiles'),
    url(r'^profile/archive', 'archive', name="experts-archive"),
    url(r'^profile/create/$', CreateProfile.as_view(), name='create-expert-profile'),
    url(r'^profile/update/(?P<pk>\d+)', UpdateProfile.as_view(), name='update-expert-profile'),
    url(r'^profile/(?P<pk>\d+)/$', HybridDetailView.as_view(model=Profile, template_name="experts/ajax.html")),
    url(r'^profile/(?P<expertname>.+)/$', 'detail', name='experts-profile'),

    # Collaborations:
    url(r'^collaborations/$', CollaborationList.as_view(), name="collaborations"),
    url(r'^collaboration/create', CreateCollaboration.as_view(), name="create-collaboration"),
    url(r'^collaboration/update/(?P<pk>\d+)', UpdateCollaboration.as_view(), name="update-collaboration"),
    url(r'^collaboration/(?P<pk>\d+)', DetailView.as_view(model=Collaboration), name="collaboration"),
    url(r'^collaboration/(?P<slug>.+)', CollaborationView.as_view(), name="collaboration")

)
