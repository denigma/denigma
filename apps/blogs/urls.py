from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
                       (r'^', 'blogs.views.index'),)
