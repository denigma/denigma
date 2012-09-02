from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView

from blog.models import Post


urlpatterns = patterns('articles.views',
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
                              model=Post,
                              template_name="articles/view.html")),
    url(r'^(?P<title>.+)$', 'view'),

    url(r'^', ListView.as_view(
                              queryset=Post.objects.filter(published=False).order_by("-created", "-id"),
                              template_name="articles/index.html")),
)
