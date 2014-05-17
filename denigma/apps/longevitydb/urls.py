from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import BrowseView, HomeView, AboutView #  SearchView,


urlpatterns = patterns('longevitydb.views',
    url(r'^$', HomeView.as_view(), name='longevitydb-home'),
    url(r'^about',AboutView.as_view(), name='longevitydb-about'),
    #url(r'^search/(?P<term>.?)', SearchView.as_view(), name='longevitydb-search'),
    url(r'^browse/(?P<model>.+)/(?P<type>.+)', BrowseView.as_view(), name='longevitydb-browse'),
    url(r'^search', 'search', name='longevitydb-search'), #SearchView.as_view()
    url(r'^browse', BrowseView.as_view(), name='longevitydb-browse'),
    url(r'^legacy', TemplateView.as_view(template_name='longevitydb.html'),
        name='longevitydb'),
)