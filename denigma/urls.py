from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"

urlpatterns = patterns("denigma.views",
    url(r"^$", 'root'),
    url(r'^meta/$', 'meta'),
    url(r'^display_meta/', 'display_meta'),
#    url(r'^', include('cms.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
)

urlpatterns += patterns("",
    url(r"^polls/", include('polls.urls')),
    url(r'^wiki/', include('wiki.urls')),
    url(r"^shorty/$", 'shorty.views.home', name='home'),
    url(r"^e/([^/]+)/", 'shorty.views.manage', name='source'),
    url(r"^a/", include(admin.site.urls)),
    url(r"^url/(\w+)/", 'shorty.views.visit', name='visit'),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^blogs/', include('blogs.urls')),
#    url(r'^links/', include('links.urls')),
#    url(r'^books/', inlcude('books.urls')),
    url(r'^contact/$', 'contact.views.contact'),
    url(r'^todos/', include('todos.urls')),
)
