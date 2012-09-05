from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('expressions.views',
    url('^$', 'index'),
)
