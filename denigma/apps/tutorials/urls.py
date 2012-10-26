from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('tutorials.views',
    url('^$', 'index', name='tutorials'),
    url('^(?P<tutorial_id>[^/]+)/view/$', 'view', name='tutorial'),
    url('^(?P<tutorial_id>[^/]+)]/edit/$', 'edit'),
    url('^development/$', 'development', name='development'),
)
