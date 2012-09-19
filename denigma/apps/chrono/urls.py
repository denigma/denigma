from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('chrono.views',
    url(r'^$', 'index', name='chrono'),
    url(r'^gettime/$', 'gettime', name='gettime'),
    url(r'^current/$', 'current_datetime', name='current_datetime'),
    url(r'^plus/(\d+)/$', 'hours_ahead', name='hours_ahead'),  # d+ = wildcard
)