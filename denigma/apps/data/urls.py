from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('data.views',
    url(r'^$', 'index', name='data'),
)