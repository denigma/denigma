from django.conf.urls.defaults import patterns

urlpatterns = patterns('gallery.views',
    (r'^$', 'index'),)
