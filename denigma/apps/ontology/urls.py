from django.conf.urls import patterns, url
from django.views.generic import DetailView

from models import Entity, Relation


urlpatterns = patterns('ontology.views',
    url(r'^$', 'index', name='ontology'),
    url(r'^load$', 'load', name='load-ontology'),
    url(r'^list$', 'list', name='ontology-list'),
    url(r'^graph$', 'graph', name='ontology-graph'),
    url(r'^entity/(?P<pk>\d+)', DetailView.as_view(model=Entity), name='ontology-entity-detail'),
    url(r'^relation/(?P<pk>\d+)', DetailView.as_view(model=Relation), name='ontology-relation-detail')
)

