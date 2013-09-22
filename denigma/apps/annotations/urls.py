# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from views import SpeciesCreate, SpeciesUpdate, TissueCreate, TissueList, GOView, GOList


urlpatterns = patterns('annotations.views',
    url(r'^$', 'index', name="annotations"),
    url(r'^bulk_upload', 'bulk_upload'),
    #url(r'^bulk_upload/data', 'bulk_upload_data'),

    # Classifications:
    url(r'^classifications/$', 'classifications', name="classifications"),
    url(r'^classification/(?P<pk>\d+)/$', 'classification'),
    url(r'^classification/add/', 'add_classification',
        name='add_classification'),
    url(r'^classification/edit/(?P<pk>\d+)/$', 'edit_classification',
        name='edit_classification'),
    url(r'^classification/delete/(?P<pk>\d+)/$', 'delete_classification',
        name='delete_classification'),

    # Species:
    url(r'^species/$', 'species', name="species"),
    url(r'^species/(?P<pk>\d+)/$', 'species_details', name='detail_species'),
    url(r'^species/archive/$', 'species_archive', name="species_archive"),
    url(r'^species/archive/(?P<pk>\d+)/$', 'species_detailed',
        name='species_detailed'),
          # DetailView.as_view(
           #  model=Taxonomy,
            # template_name='annotations/species_detailed')
    url(r'^species/edit/(?P<pk>\d+)/$',
        login_required(SpeciesUpdate.as_view()), name='update-species'),
    url(r'^species/add/$', SpeciesCreate.as_view(), name='create-species'),

    url(r'^go/$', GOView.as_view()),
    url(r'^go_list/$', GOList.as_view()),


    # Tissues:
    url(r'^tissue/table/$', 'tissue_table', name='tissue_table'),
    url(r'^tissues/$', TissueList.as_view(), name="tissues"),
    url(r'^tissue/(?P<pk>\d+)/$', 'tissue', name="tissue"),
    url(r'^tissue/archive', 'tissue_archive', name="tissue_archive"),
    url(r'^tissue/add/$', 'add_tissue', name='add_tissue'),
    url(r'^tissue/edit/(?P<pk>\d+)/$', 'edit_tissue', name='edit_tissue'),
    url(r'^tissue/create/$', TissueCreate.as_view(), name='create_tissue'),
    url(r'^tissue/delete/(?P<pk>\d+)', 'delete_tissue', name='delete_tissue'),
    url(r'^tissue/hierarchy/$', 'tissue_hierarchy', name='tissue_hierarchy'),
    url(r'^tissue/(?P<name>.+)/$', 'tissue', name='tissue'),
)
#234567891123456789212345678931234567894123456789512345678961234567897123456789
