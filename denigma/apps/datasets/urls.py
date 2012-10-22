"""Dataset urls."""
from django.conf.urls import patterns, url
from django.views.generic import DetailView

from models import Reference


urlpatterns = patterns('datasets.views',
    url(r'^$', 'index', name='annotations'),
    url(r'^references/update', 'update_references'),
    url(r'^references/duplicates', 'duplicates'),
    url(r'^references/update', 'update_references'),
    url(r'^references', 'references'),
    url(r'reference/(?P<pk>\d+)', DetailView.as_view(model=Reference), name='detail-reference'),
    url(r'^changes', 'changes', name='changes'),
    url(r'^epistasis', 'epistasis', name='epistasis'),
)
