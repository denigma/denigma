from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from lifespan.views import VarianceDetail, VariantDetail, FactorDetail, Population, StudyType

from views import BrowseView, HomeView, AboutView #  SearchView,

from datasets.views import detail


urlpatterns = patterns('longevitydb.views',
    url(r'^$', HomeView.as_view(), name='longevitydb-home'),
    url(r'^about',AboutView.as_view(), name='longevitydb-about'),
    #url(r'^search/(?P<term>.?)', SearchView.as_view(), name='longevitydb-search'),
    url(r'^browse/(?P<model>.+)/(?P<type>.+)', csrf_exempt(BrowseView.as_view()), name='longevitydb-browse'),
    url(r'^search/$', 'search', name='longevitydb-search'), #SearchView.as_view()
    url(r'^search/(?P<keyword>.+)/', 'search', name='longevitydb-search'), #SearchView.as_view()

    url(r'^browse', csrf_exempt(BrowseView.as_view()), name='longevitydb-browse'),
    url(r'^legacy', TemplateView.as_view(template_name='longevitydb.html'),
        name='longevitydb'),
    url(r'^longevitydb', HomeView.as_view(), name='longevitydb-longevitydb'),
    url(r'^detail/(?P<pk>\d+)/$', VariantDetail.as_view(template_name='longevitydb/detail.html'), name='lvdb-variant'),
    url(r'^factor_detail/(?P<pk>\d+)/$', FactorDetail.as_view(template_name='longevitydb/factor_detail.html'), name='lvdb-factor_detail'),
    url(r'^population_detail/(?P<pk>\d+)/$', DetailView.as_view(model=Population, template_name='longevitydb/population_detail.html'), name='lvdb-population_detail'),
    url(r'^studytype_detail/(?P<pk>\d+)/$', DetailView.as_view(model=StudyType, template_name='longevitydb/studytype_detail.html'), name='lvdb-studytype_detail'),
    url(r'reference_detail/(?P<pk>\d+)', detail, {'template':'longevitydb/reference_detail.html'}, name='lvdb-reference_detail'),

)