from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('lifespan.views',
    (r'^genage/describe', 'describe'),
    (r'^genage/functional_description', 'functional_description'),
    (r'^genage/integrity', 'integrity'),
    (r'^(?P<table>\w+)/replace/(?P<field>\w+)/(?P<term>.+)/(?P<by>.+)/$', 'replace'), #
    (r'^gendr/dump', 'dump'),
    (r'^$', 'index'),
)
