from django.conf.urls import patterns,  url
from django.views.generic import ListView, DetailView

from data.models import Entry


urlpatterns = patterns('articles.views',
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
                              model=Entry,
                              context_object_name='article',
                              template_name="articles/view.html")),
    url(r'^(?P<title>.+)$', 'view'),

    url(r'^', ListView.as_view(
                              queryset=Entry.objects.filter(published=False).order_by("-created", "-id"),
                              template_name="articles/index.html")),
)
