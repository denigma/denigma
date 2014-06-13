from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from lifespan.views import VarianceDetail, VariantDetail

from views import BrowseView, HomeView, AboutView #  SearchView,


urlpatterns = patterns('longevitydb.views',
    url(r'^$', HomeView.as_view(), name='longevitydb-home'),
    url(r'^about',AboutView.as_view(), name='longevitydb-about'),
    #url(r'^search/(?P<term>.?)', SearchView.as_view(), name='longevitydb-search'),
    url(r'^browse/(?P<model>.+)/(?P<type>.+)', csrf_exempt(BrowseView.as_view()), name='longevitydb-browse'),
    url(r'^search', 'search', name='longevitydb-search'), #SearchView.as_view()
    url(r'^browse', csrf_exempt(BrowseView.as_view()), name='longevitydb-browse'),
    url(r'^legacy', TemplateView.as_view(template_name='longevitydb.html'),
        name='longevitydb'),
    url(r'^longevitydb', HomeView.as_view(), name='longevitydb-longevitydb'),
    #url(r'^detail/(?P<name>.+)/$', VarianceDetail.as_view(template_name='longevitydb/detail.html'), name='variant'),
    url(r'^detail/(?P<pk>\d+)/$', VariantDetail.as_view(template_name='longevitydb/detail.html'), name='variant'),
)