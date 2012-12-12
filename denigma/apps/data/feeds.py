from django.contrib.syndication.views import Feed

from models import Entry


class EntryFeed(Feed):
    title = "Denigma"
    description = "The Digital Enigma."
    link = "/data/feed/"

    def items(self):
        return Entry.objects.filter(published=True).order_by("-created")[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.brief()

    def item_link(self, item):
        return u"/data/entry/%s" % item.pk
