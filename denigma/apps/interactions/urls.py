from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('interactions.views',
    url('^$', 'index'),
)
