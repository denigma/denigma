from django.contrib.syndication.views import Feed

from models import Post


class BlogFeed(Feed):
    title = "Denigma"
    description = "The Digital Enigma."
    link = "/blog/feed/"

    def items(self):
       return Post.objects.filter(published=True).order_by("-created")[:25]

    def item_title(self, item):
       return item.title

    def item_description(self, item):
       return item.text

    def item_link(self, item):
       return u"/blog/%d" % item.id


class ArchiveFeed(Feed):
    title = 'Archive Feed'
    description = 'Archive Feed'
    link = '/blog/archive/'

    def items(self):
        return Post.objects.filter(published=True).order_by('-id')[:25]

    def item_link(self):
        return '/blog/archive'

    def item_title(self, item):
        return item.title

    def item_description(self):
        return ""
