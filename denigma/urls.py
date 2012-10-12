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
    url(r'^$', 'home', name="home"),
    url(r'^google(?P<term>\w+)', 'google'),
    #url(r'^search/(?P<term>.*)', 'search'), # Side-wide search
    url(r'^search/', include('haystack.urls')),
    url(r'^content/', 'content', name='content'),
    url(r'^404/$', direct_to_template, {'template':'404.html'}, name='404'),
    url(r'^500/$', direct_to_template, {'template':'500.html'}, name='505'),
#    url(r'^', include('cms.urls')),
)

urlpatterns += patterns("",
    url(r"^homepage", direct_to_template, {"template": "homepage.html",}, name="homepage"), # For fast static rendering. 
    url(r'^home/', include('home.urls')),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', include(admin.site.urls)),
    url(r'^about/', include("about.urls")),
    url(r'^account/', include("account.urls")),#, pinax.apps.account.urls")),
    url(r'^openid/', include(PinaxConsumer().urls)),
    url(r'^profiles/', include("idios.urls")),
    url(r'^notices/', include("notification.urls")),
    url(r'^announcements/', include("announcements.urls")),
    url(r'^polls/', include('polls.urls')),
    url(r'^wiki/', include('wiki.urls')),
    url(r'^shorty/$', 'shorty.views.home'),
    url(r'^e/([^/]+)/', 'shorty.views.manage', name='source'),
    url(r'^url/(\w+)/', 'shorty.views.visit', name='visit'),
    url(r'^media/', include('media.urls')),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^news/$', include('news.urls')), # Blogs is currently functioning as news medium.
    #url(r'^links/', include('links.urls')),
    url(r'^books/', include('books.urls')),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^todos/', include('todos.urls')),
    url(r'^experts/', include('experts.urls')),
    url(r'^pastebin/', include('pastebin.urls')),
    url(r'^grappeli/', include('grappelli.urls')),
    url(r'^tutorials/', include('tutorials.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^annotations/', include('annotations.urls')),
    url(r'^interactions/', include('interactions.urls')),
    url(r'^expressions/', include('expressions.urls')),
    url(r'^datasets/', include('datasets.urls')),
    url(r'^lifespan/', include('lifespan.urls')),
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
       {'url': '/media/img/favicon.ico'}), # Site icon
    url(r'^time/', include('chrono.urls')),
    url(r'^meta/', include('meta.urls')),
    url(r'^aspects/', include('aspects.urls')),
    #
    url(r'^data/', include('data.urls')),
    url(r'^eva/', include('eva.urls')),
)
if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'', include("staticfiles.urls")),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
