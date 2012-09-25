from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView

from models import Measurement


urlpatterns = patterns('lifespan.views',
    url(r'^$', 'index', name='lifespan'),

    url(r'^studies/$', 'studies', name='studies'),
    url(r'^study/(?P<pk>\d+)', 'study'),
    url(r'^studies/add', 'add_studies', name='add_studies'),
    url(r'^study/edit/(?P<pk>\d+)', 'edit_study'),
    url(r'^study/delete/(?P<pk>\d+)', 'delete_study'),
    url(r'^studies/archive/$', 'studies_archive', name='studies_archive'),

    url(r'^experiments/$', 'experiments', name='experiments'),
    url(r'^experiment/(?P<pk>\d+)', 'experiment',),
    url(r'^experiment/add/(?P<pk>\d*)', 'add_experiment', name='add_experiment'),
    url(r'^experiment/edit/(?P<pk>\d+)', 'edit_experiment'),
    url(r'^experiment/delete/(?P<pk>\d+)', 'delete_experiment'),

    # Measurements:
    #url(r'^measurements/$', 'measurements', name='measurements'),
    url(r'^measurements/$',
        ListView.as_view(queryset=Measurement.objects.all(),
            template_name='lifespan/measurements.html'), name='measurements'),
    url(r'^measurement/(?P<pk>\d+)',
        DetailView.as_view(model=Measurement,
            template_name='lifespan/measurement.html')),

    url(r'^comparisions/$', 'comparisions', name='comparisions'),
    url(r'^comparision/(?P<pk>/d+)', 'comparision'),
    url(r'^comparision/add', 'add_comparision', name='add_comparision'),
    url(r'^comparision/edit/(?P<pk>/d+)', 'edit_comparision'),

    url(r'^interventions/$', 'interventions', name='interventions'),
    url(r'^intervention/(?P<pk>/d+)', 'intervention'),
    url(r'^intervention/add', 'add_intervention', name='add_intervention'),
    url(r'^intervention/edit/(?P<pk>/d+)', 'edit_intervention'),

    url(r'^factors/$', 'factors', name='factors'),
    url(r'^factor/(?P<pk>\d+)/$', 'factor'),
    url(r'^factor/add/$', 'add_factor', name='add_factor'),
    url(r'^factor/edit(?P<pk>\d+)/$', 'edit_factor'),

    url(r'^epistasis/$', 'epistasis'),
    url(r'^regimen/$', 'regimen'),
    url(r'^assay/$', 'assay'),
    url(r'^manipulation/$', 'manipulation'),
    url(r'^type/$', 'type'),

    url(r'^genage/describe', 'describe'),
    url(r'^genage/functional_description', 'functional_description'),
    url(r'^genage/integrity', 'integrity'),
    url(r'^(?P<table>\w+)/replace/(?P<field>\w+)/(?P<term>.+)/(?P<by>.+)/$', 'replace'),
    url(r'^gendr/dump', 'dump'),


)

#234567891123456789212345678931234567894123456789512345678961234567897123456789