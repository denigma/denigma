from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('tutorials.views',
    url('^$', 'index'),
)
