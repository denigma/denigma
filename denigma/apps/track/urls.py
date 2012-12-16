from django.conf.urls import patterns, url


urlpatterns = patterns("track.views",
    url(r'^refresh/$', 'update_active_users', name='track-refresh-active-users'),
    url(r'refresh/json/$', 'get_active_users', name='track-get-active-users'),
)

