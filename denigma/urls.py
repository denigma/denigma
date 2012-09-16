from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from staticfiles.urls import staticfiles_urlpatterns

from pinax.apps.account.openid_consumer import PinaxConsumer

from sitemaps import SiteMap, SiteSiteMap


sitemaps = {
   'Denigma': SiteMap,
   'pages': SiteSiteMap(['contact', 'archive']),
}

handler500 = "pinax.views.server_error"

urlpatterns = patterns("denigma.views",
    url(r'^$', 'root', name="root"),
    url(r'^meta/$', 'meta'),
    url(r'^display_meta/', 'display_meta'),
    url('^time/$', 'current_datetime'),
    url(r'^time/plus/(\d+)/$', 'hours_ahead'),  # d+ = wildcard
    url(r'^google(?P<term>\w+)', 'google'),
    #url(r'^search/(?P<term>.*)', 'search'), # Side-wide search
    url(r'^search/', include('haystack.urls')),
#    url(r'^', include('cms.urls')),
)

urlpatterns += patterns("",
    url(r"^homepage", direct_to_template, {"template": "homepage.html",}, name="home"), # For fast static rendering. 
    url(r'^home/', include('home.urls')),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', include(admin.site.urls)),
    url(r'^about/', include("about.urls"), name='about'),
    url(r'^account/', include("account.urls")),#, pinax.apps.account.urls")),
    url(r'^openid/', include(PinaxConsumer().urls)),
    url(r'^profiles/', include("idios.urls")),
    url(r'^notices/', include("notification.urls")),
    url(r'^announcements/', include("announcements.urls")),
    url(r'^polls/', include('polls.urls'), name='polls'),
    url(r'^wiki/', include('wiki.urls'), name='wiki'),
    url(r'^shorty/$', 'shorty.views.home'),
    url(r'^e/([^/]+)/', 'shorty.views.manage', name='source'),
    url(r'^url/(\w+)/', 'shorty.views.visit', name='visit'),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^blog/', include('blog.urls')),
    #url(r'^news/', include('news.urls')), # Blogs is currently functioning as news medium.
    #url(r'^links/', include('links.urls')),
    #url(r'^books/', inlcude('books.urls')),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^todos/', include('todos.urls')),
    url(r'^experts/', include('experts.urls')),
    url(r'^pastebin/', include('pastebin.urls')),
    url(r'^grappeli/', include('grappelli.urls')),
    url(r'^tutorials/', include('tutorials.urls'), name="tutorials"),
    url(r'^articles/', include('articles.urls'), name="articles"),
    url(r'^annotations/', include('annotations.urls'), name="annotations"),
    url(r'^interactions/', include('interactions.urls'), name="interactions"),
    url(r'^expressions/', include('expressions.urls'), name="expressions"),
    url(r'^datasets/', include('datasets.urls'), name="datasets"),
    url(r'^lifespan/', include('lifespan.urls'), name="lifespan"),
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
       {'url': '/media/img/favicon.ico'}), # Site icon
)
if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'', include("staticfiles.urls")),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
