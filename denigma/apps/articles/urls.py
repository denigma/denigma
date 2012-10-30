from django.conf.urls import patterns,  url
from django.views.generic import ListView, DetailView
from django.db.models import Q

from data.models import Entry


urlpatterns = patterns('articles.views',
    url(r'^reference/(?P<slug>.+)', 'reference', name='reference'),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
            model=Entry,
            context_object_name='article',
            template_name="articles/view.html"),
        name='article'),
    url(r'^(?P<title>.+)$', 'view', name='article'),
    url(r'^', ListView.as_view(
        queryset=Entry.objects.filter(
            Q(tagged__name="article") |
            Q(categories__name="Article")).order_by("-created", "-id").distinct(),
        template_name="articles/index.html"),
        name='articles'),

    #url(r'output/(?P<pk>)', output)
)
