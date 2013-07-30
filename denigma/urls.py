"""Global URLconf."""
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from staticfiles.urls import staticfiles_urlpatterns

from pinax.apps.account.openid_consumer import PinaxConsumer

from sitemaps import SiteMap, SiteSiteMap

#from haystack.views import SearchView
#from forms import DateRangeSearchForm

from tastypie.api import Api
from lifespan.api.resources import FactorResource


lifespan_api = Api(api_name='lifespan')
lifespan_api.register(FactorResource())
#factor_resource = FactorResource()

sitemaps = {
   'Denigma': SiteMap,
   'pages': SiteSiteMap(['contact', 'archive']),
}

handler500 = "pinax.views.server_error"

urlpatterns = patterns("denigma.views",
    url(r'^$', 'home', name="home"),
    #url(r'^search/', include('haystack.urls')),
    #url(r'^search/', SearchView(form_class=DateRangeSearchForm)),
    url(r'^content/', 'content', name='content'),
    url(r'^404/$', TemplateView.as_view(), {'template':'404.html'}, name='404'),
    url(r'^500/$', TemplateView.as_view(), {'template':'500.html'}, name='505'),
    url(r'^repository/$', 'repository', name='repository'),
    url(r'^api/', include(lifespan_api.urls))
    #url(r'api/', include(factor_resource.urls)),
    #url(r'^google(?P<term>\w+)', 'google'),
    #url(r'^search/(?P<term>.*)', 'search'), # Side-wide search
#    url(r'^', include('cms.urls')),
)

urlpatterns += patterns("",
    url(r"^homepage", TemplateView.as_view(), {"template": "homepage.html",}, name="homepage"), # For fast static rendering.
    url(r'^home/', include('home.urls')),

    # Admin
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', include(admin.site.urls)),
    url(r'^grappeli/', include('grappelli.urls')),

    # User
    url(r'^account/', include("account.urls")),#, pinax.apps.account.urls")),
    url(r'^openid/', include(PinaxConsumer().urls)),
    url(r'^notices/', include("notification.urls")),
    url(r'^announcements/', include("announcements.urls")),
    url(r'^avatar/', include('avatar.urls')), # django-avatar: Representative user images

    # Comments
    url(r'^comments/', include('fluent_comments.urls')), #django.contrib.comments.urls')),

    # Filtering
    #url(r'^ajax_filtered_fields/', include('ajax_filtered_fields.urls')),
    #url(r'^dynamic-media/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    url(r'^profiles/', include("idios.urls")),
    url(r'^aspects/', include('aspects.urls')),

    url(r'^polls/', include('polls.urls')),
    url(r'^questionnaire', include('questionnaire.urls')),
    url(r'^donate/', include('donation.urls')),
    url(r'^gallery/', include('media.urls')),

    # Data Unit
    url(r'^wiki/', include('wiki.urls')),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^data/', include('data.urls')),
    url(r'^news/$', include('news.urls')), # Data entry is currently functioning as news medium.
    url(r'^tutorials/', include('tutorials.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^ontology/', include('ontology.urls')),

    # Links
    url(r'^shorty/$', 'shorty.views.home', name='sURL'),
    url(r'^e/([^/]+)/', 'shorty.views.manage', name='source'),
    url(r'^url/(\w+)/', 'shorty.views.visit', name='visit'),
    url(r'^links/', include('links.urls')),

    # Duties
    url(r'^duties/', include('duties.urls')),
    url(r'^tasks/', include('tasks.urls')),
    #url(r'^todo/', include('todo.urls')),
    url(r'^todos/', include('todos.urls')),
    url(r'^quests/', include('quests.urls')),
    url(r'^task/', include('task.urls')),

    # Communication
    url(r'^pastebin/', include('pastebin.urls')),
    url(r'^channel/', include('channel.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^video/', include('video.urls')),
    url(r'^c/', TemplateView.as_view(template_name='chat.html')),

    # Integrator
    url(r'^annotations/', include('annotations.urls')),
    url(r'^interactions/', include('interactions.urls')),
    url(r'^expressions/', include('expressions.urls')),
    url(r'^datasets/', include('datasets.urls')),
    url(r'^lifespan/', include('lifespan.urls')),

    # Standards
    url(r'^about/', include("about.urls")),
    url(r'^contact/$', 'contact.views.contact', name='contact'),
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
       {'url': '/media/img/favicon.ico'}), # Site icon

    # In Progress
    url(r'^experts/', include('experts.urls')),
    url(r'^books/', include('books.urls')),
    url(r'^time/', include('chrono.urls')),
    url(r'^meta/', include('meta.urls')),
    url(r'^add/', include('add.urls')),
    url(r'^eva/', include('eva.urls')),
    url(r'^network/', include('network.urls')),

    # Sites
    url(r'^alliance/', include('alliance.urls')),
    url(r'^immuno/', include('immuno.urls')),
)
if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'', include("staticfiles.urls")),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
