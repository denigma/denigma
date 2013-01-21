from django.conf.urls import patterns, url

from views import IndexView, DetailView, AboutView, ContactView


urlpatterns = patterns('immuno.views',
    url(r'^$', IndexView.as_view(),  name='immuno'),
    url(r'^about/$',AboutView.as_view(), {'slug':'about-immunology-lab'}, name='immuno-about'),
    url(r'^contact/$', ContactView.as_view(), {'slug':'contact-immunology-lab'}, name='immuno-contact'),
    url(r'^(?P<slug>.+)', DetailView.as_view(), name='immuno-entry'),
)