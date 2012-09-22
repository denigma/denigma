from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('tutorials.views',
    url('^$', 'index'),
    url('^(?P<tutorial_id>[^/]+)/view/$', 'view'),
    url('^(?P<tutorial_id>[^/]+)]/edit/$', 'edit'),
    url('^development/$', 'development', name='development'),
)
