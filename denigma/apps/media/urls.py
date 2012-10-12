from django.conf.urls.defaults import patterns

urlpatterns = patterns('media.views',
    (r'^$', 'index'),)
