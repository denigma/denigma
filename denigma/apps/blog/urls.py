from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed

from models import Post


class BlogFeed(Feed):
    title = "Denigma"
    description = "The digital Enigma."
    link = "/blog/feed/"

    def items(self):
       return Post.objects.all().order_by("created")[:2]
    def item_title(self, item):
       return item.title
    def item_description(self, item):
       return item.body
    def item_link(self, item):
       return u"/blog/%d" % item.id

urlpatterns = patterns('blog.views',
    url(r'^$', ListView.as_view(
                              queryset=Post.objects.all().order_by("-created"),
                              template_name="blog/index.html")),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
                              model=Post,
                              template_name="blog/post.html")),
    url(r'archive/$', ListView.as_view(
                              queryset=Post.objects.all().order_by("-created"),
                              template_name="blog/archive.html")),
    url(r'^tag/(?P<tag>\w+)$', 'tagpage'),
    url(r'^feed/$', BlogFeed()),
)
