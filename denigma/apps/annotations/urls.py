# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from models import Taxonomy
from views import SpeciesCreate, SpeciesUpdate


urlpatterns = patterns('annotations.views',
    url(r'^classifications/$', 'classifications', name="classification"), 
    url(r'^classification/(?P<pk>\d+)/$', 'classification'),
    url(r'^species/$', 'species', name="species"),
    url(r'^species/(?P<pk>\d+)/$', 'species_details'),
    url(r'^species/archive/$', 'species_archive', name="species_archive"),
    url(r'^species/archive/(?P<pk>\d+)/$', 'species_detailed'),
          # DetailView.as_view(
           #  model=Taxonomy,
            # template_name='annotations/species_detailed')
    url(r'^species/edit/(?P<pk>\d+)/$', login_required(SpeciesUpdate.as_view())),
    url(r'^species/add/$', SpeciesCreate.as_view()),
    url(r'^tissues/$', 'tissues', name="tissues"),
    url(r'^tissue/(?P<pk>\d+)/$', 'tissue'),
    url(r'^tissue/archive', 'tissue_archive', name="tissue_archive"),
    url(r'^$', 'index', name="annotations"),
    url(r'^bulk_upload', 'bulk_upload'),
    #url(r'^bulk_upload/data', 'bulk_upload_data'),
)

