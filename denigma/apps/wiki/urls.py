from django.conf.urls.defaults import patterns


urlpatterns = patterns('wiki.views',
    (r'^page/(?P<page_name>[^/]+)/edit/$', 'edit_page'),
    (r'^page/(?P<page_name>[^/]+)/save/$', 'save_page'),                      
    (r'^page/(?P<page_name>[^/]+)/$', 'view_page'),
    (r'^tag/(?P<tag_name>[^/]+)/$', 'view_tag'),
)
