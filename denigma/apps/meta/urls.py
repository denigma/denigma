from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('meta.views',
    url(r'^$', 'index', name="meta"),
    url(r'^activity/(?P<pk>.+)/$', 'activity'),
    url(r'^data/$', 'data'),
    url(r'^display', 'display'),
)