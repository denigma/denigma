from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('eva.views',
    url('^$', 'index', name='eva'),
    url('^tf_idf/(?P<keyword>.+)', 'tf_idf', name='tf_idf')
)
