from django.conf.urls import patterns, url


urlpatterns = patterns('ontology.views',
    url(r'^$', 'index', name='ontology'),
    url(r'^load$', 'load', name='load-ontology'),
    url(r'^graph$', 'graph', name='ontology-graph')
)

