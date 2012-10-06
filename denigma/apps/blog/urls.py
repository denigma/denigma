from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed

from views import PostListView

from models import Post
from feeds import BlogFeed


urlpatterns = patterns('blog.views',
    url(r'^$', PostListView.as_view(
                              queryset=Post.objects.filter(published=True).order_by("-created", "-id"),
                              template_name="blog/index.html"), name='blog'),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
                              model=Post,
                              template_name="blog/view.html")),
    url(r'^add/$', 'add', name='add_post'),
    url(r'^edit/(?P<pk>\d+)', 'edit', name='edit_post'),
    url(r'archive/$', ListView.as_view(
                              queryset=Post.objects.filter(published=True).order_by("-created", "-id"),
                              template_name="blog/archive.html"), name='archive'),
    url(r'^tag/(?P<tag>\w+)$', 'tagpage'),
    url(r'^feed/$', BlogFeed(), name='feed'),
    url(r'^articles/$', ListView.as_view(
                              queryset=Post.objects.filter(published=False).order_by("-created", "-id"),
                              template_name="blog/articles.html"), name='articles'),
    url(r'^list/$', 'list', name='post-list'), # Uses django-filter.
    url(r'^admin/$', 'custom_admin_view'),
)
