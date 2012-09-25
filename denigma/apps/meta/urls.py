from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('meta.views',
    url(r'^$', 'index', name="meta"),
    url(r'^activity/(?P<pk>.+)/$', 'activity'),
    url(r'^data/$', 'data'),
    url(r'^display', 'display'),
    url(r'^diff/(?P<pk>\d+)/$', 'diff', name='diff'),
    url(r'^difference/$', 'difference', name='difference'),
)