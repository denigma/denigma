from django.conf.urls.defaults import patterns


urlpatterns = patterns('home.views',
   (r'^$', 'index'),
   (r'^base', 'base'),
   (r'^page', 'page'),
)
