"""Dataset urls."""
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import ReferenceList, ReferenceCreate, ReferenceUpdate



urlpatterns = patterns('datasets.views',
    url(r'^$', 'index', name='datasets'),
    url(r'^references/update', 'update_references'),
    url(r'^reference/create', ReferenceCreate.as_view(), name='create-reference'),
    url(r'^reference/update/(?P<pk>\d+)', login_required(ReferenceUpdate.as_view()), name='update-reference'),
    url(r'^reference/autoupdate/(?P<pk>\d+)', 'autoupdate_reference', name='autoupdate_reference'),
    url(r'^references/duplicates', 'duplicates', name='duplicates'),
    url(r'^references/update', 'update_references'),
    url(r'^references/archive', 'references_archive', name='references_archive'),
    url(r'^references', ReferenceList.as_view(), name='references'),
    url(r'reference/(?P<pk>\d+)', 'detail', name='detail-reference'),
    url(r'^changes', 'changes', name='changes'), # Rename to "deltas"
)
