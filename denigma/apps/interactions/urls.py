from django.conf.urls import patterns, url

from views import InteractionList, InteractionRDF

urlpatterns = patterns('interactions.views',
    url('^$', 'index', name='interactions'),
    url('^update/(?P<db>.+)', 'update', name='update-interactions'),
    url('^integrator', 'integrator', name='interaction-integrator'),
    url('^table', InteractionList.as_view(), name='interaction-table'),
    url('^rdf', InteractionRDF.as_view(), name='interaction-rdf'),
)
