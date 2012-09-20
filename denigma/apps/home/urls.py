from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('home.views',
   url(r'^$', 'index'),
   url(r'^base', 'base'),
   url(r'^page', 'page'),
)
