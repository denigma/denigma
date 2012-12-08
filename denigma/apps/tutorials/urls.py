from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('tutorials.views',
    url('^$', 'index', name='tutorials'),
    url('^(?P<pk>[^/]+)/view/$', 'view', name='tutorial'),
    url('^(?P<pk>[^/]+)]/edit/$', 'edit'),
    url('^development/$', 'development', name='development'),
)
