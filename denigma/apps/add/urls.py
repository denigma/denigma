from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^category/?$', 'links.views.newCategory'),
)