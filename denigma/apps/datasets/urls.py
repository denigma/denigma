"""Dataset urls."""
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('datasets.views',
    url(r'^$', 'index', name='annotations'),
    url(r'^references/update', 'update_references'),
    url(r'^references/duplicates', 'duplicates'),
    url(r'^references/update', 'update_references'),
    url(r'^references', 'references'),
    url(r'^changes', 'changes', name='changes'),
    url(r'^epistasis', 'epistasis', name='epistasis'),
)
