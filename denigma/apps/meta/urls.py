from django.conf.urls import patterns, url


urlpatterns = patterns('meta.views',
    url(r'^$', 'index', name="meta"),
    url(r'^activity/(?P<pk>.+)/$', 'activity'),
    url(r'^data/$', 'data', name='meta-data'),
    url(r'^display', 'display'),
    url(r'^diff/(?P<pk>\d+)/$', 'diff', name='diff'),
    url(r'^difference/$', 'difference', name='difference'),
    url(r'^links/$', 'links', name='meta-links'),
    url(r'^objects/(?P<link>.+)', 'objects', name='meta-objects'),
)