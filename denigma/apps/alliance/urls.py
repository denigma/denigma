from django.conf.urls import patterns, url

from views import DataUnitView, ProjectView, DataList, ProjectDetail


urlpatterns = patterns('alliance.views',
    url(r'^$', 'index', name='alliance-home'),
    url(r'^data/list/$', DataList.as_view(paginate_by=5), name='alliance-data'),
    url(r'^data/entry/(?P<slug>.+)', DataUnitView.as_view(), name='alliance-entry'),
    url(r'^about/$', DataUnitView.as_view(), {'slug':'about-the-alliance'}, name='alliance-about'),
    url(r'^manifesto/$', DataUnitView.as_view(), {'slug':'ila-manifesto'}, name='alliance-manifesto'),
    url(r'^take-action/$', DataUnitView.as_view(), {'slug': 'take-action'}, name='alliance-take-action'),
    url(r'^projects/$', ProjectView.as_view(), name='alliance-projects'),
    url(r'^project/(?P<pk>\d+)', ProjectDetail.as_view(), name='alliance-project'),
)