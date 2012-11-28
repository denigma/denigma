from django.conf.urls import patterns, url


urlpatterns = patterns('duties.views',
    url(r'^$', 'index', name='duties'),
)