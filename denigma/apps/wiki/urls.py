from django.conf.urls import patterns, url


urlpatterns = patterns('wiki.views',
    url(r'^page/(?P<page_name>[^/]+)/edit/$', 'edit_page'),
    url(r'^page/(?P<page_name>[^/]+)/save/$', 'save_page'),
    url(r'^page/(?P<page_name>[^/]+)/$', 'view_page'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', 'view_tag'),
    url(r'^$', 'view_page', {'page_name':'Start'}, name='wiki'),
)
