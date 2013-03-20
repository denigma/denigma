from django.conf.urls import patterns, url
from django.views.generic import list_detail

from models import Announcement

from views import  announcement_hide, announcement_list
from views import detail, dismiss

from views import CreateAnnouncementView, UpdateAnnouncementView
from views import DeleteAnnouncementView, AnnouncementListView


announcement_detail_info = {
    "queryset": Announcement.objects.all(),
}

urlpatterns = patterns("",
#    url(r'^(?P<object_id>\d+)/$', list_detail.object_detail,
#        announcement_detail_info, name="announcement_detail"),
    url(r'^(?P<object_id>\d+)/hide/$', announcement_hide,
        name="announcement_hide"),

    url(r'^$', announcement_list, name="announcement_home"),
    url(r'^$', AnnouncementListView.as_view(), name="announcements_list"),
    url(r'^announcement/create/$', CreateAnnouncementView.as_view(), name="announcement_create"),
    url(r'^announcement/(?P<pk>\d+)/$', detail, name="announcement_detail"),
#    url(r'^announcement/(?P<pk>\d+)/hide/$', dismiss, name="announcement_dismiss"),
    url(r'^announcement/(?P<pk>\d+)/update/$', UpdateAnnouncementView.as_view(), name="announcement_update"),
    url(r'^announcement/(?P<pk>\d+)/delete/$', DeleteAnnouncementView.as_view(), name="announcement_delete"),
)