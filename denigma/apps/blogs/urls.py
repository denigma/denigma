from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('blogs.views',
    url(r'^/$', 'index', name='blogs'),
)

