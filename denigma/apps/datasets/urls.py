"""Dataset urls."""
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('datasets.views',
    url(r'^references/update', 'update_references'),
    url(r'^references/duplicates', 'duplicates'),
    url(r'^references', 'references'),

    url(r'^$', 'index'),	

)
