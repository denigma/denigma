from django.conf.urls import patterns,  url
from django.views.generic import DetailView

from data.models import Entry

from views import ArticleList


urlpatterns = patterns('articles.views',
    url(r'^reference/(?P<slug>.+)', 'reference', name='reference'),
    url(r'^connect/(?P<slug>.+)', 'connect', name='connect'),
    url(r'^presentation/(?P<slug>.+)', 'presentation', name='presentation'),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
            model=Entry,
            context_object_name='article',
            template_name="articles/view.html"),
        name='article'),
    url(r'^(?P<title>.+)$', 'view', name='article'),
    url(r'^', ArticleList.as_view(), name='articles'),
    #url(r'output/(?P<pk>)', output)
)
