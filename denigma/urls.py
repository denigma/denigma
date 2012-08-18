from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from staticfiles.urls import staticfiles_urlpatterns

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"

urlpatterns = patterns("denigma.views",
    url(r"^root/", 'root'),
    url(r'^meta/$', 'meta'),
    url(r'^display_meta/', 'display_meta'),
    url('^time/$', 'current_datetime'),
    url(r'^time/plus/(\d+)/$', 'hours_ahead'),  # d+ = wildcard
    url(r'^pastebin/', include('pastebin.urls')),
#    url(r'^', include('cms.urls')),
)


urlpatterns += patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', include("about.urls")),
    url(r'^account/', include("pinax.apps.account.urls")),
    url(r'^openid/', include(PinaxConsumer().urls)),
    url(r'^profiles/', include("idios.urls")),
    url(r'^notices/', include("notification.urls")),
    url(r'^announcements/', include("announcements.urls")),
)

urlpatterns += patterns("",
    url(r'^polls/', include('polls.urls')),
    url(r'^wiki/', include('wiki.urls')),
    
    url(r'^shorty/$', 'shorty.views.home'),
    url(r'^e/([^/]+)/', 'shorty.views.manage', name='source'),
    url(r'^a/', include(admin.site.urls)),
    url(r'^url/(\w+)/', 'shorty.views.visit', name='visit'),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^blogs/', include('blogs.urls')),
#    url(r'^links/', include('links.urls')),
#    url(r'^books/', inlcude('books.urls')),
    url(r'^contact/$', 'contact.views.contact'),
    url(r'^todos/', include('todos.urls')),
    #url(r'^experts/', include('experts.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'', include("staticfiles.urls")),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
