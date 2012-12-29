from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^category/?$', 'links.views.newCategory', name="new-category"),
    url(r'^countries/?$', 'links.views.newCountry', name="new-country"),
    url(r'^contacts/?', 'experts.views.newProfile', name="new-profile"),
)