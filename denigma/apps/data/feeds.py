from django.contrib.syndication.views import Feed

from models import Entry, Change, Relation, Alteration, Category


class EntryFeed(Feed):
    title = "Denigma Data Entries"
    description = "Denigma's most fundamental data unit."
    link = "/data/entry/feed/"

    def items(self):
        return Entry.objects.filter(published=True).order_by("-created")[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.brief()

    def item_link(self, item):
        return u"/data/entry/%s" % item.slug


class ChangeFeed(Feed):
    title = "Denigma Data Changes"
    description = "Changes of Denigma's data entries."
    link = "/data/change/feed/"

    def items(self):
        return Change.objects.filter(of__published=True).order_by("-at")[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.brief()

    def item_link(self, item):
        return u"/data/change/%s" % item.pk


class RelationFeed(Feed):
    title = "Denigma Data Relations"
    description = "Relations between Denigma's data entries."
    link = "/data/relation/feed/"

    def items(self):
        return Relation.objects.all().order_by("-created")[:25]

    def item_title(self, item):
        return item

    def item_description(self, item):
        return"<br>".join((item.fr.brief(), item.be.brief(), item.to.brief()))

    def item_link(self, item):
        return u"/data/relation/%s" % item.pk


class AlterationFeed(Feed):
    title = "Denigma Data Alterations"
    description = "Alterations of Denigma's data relations."
    link = "/data/alteration/feed/"

    def items(self):
        return Alteration.objects.all().order_by("-at")[:25]

    def item_title(self, item):
        return item

    def item_description(self, item):
        return "<br>".join((item.fr.brief(), item.be.brief(), item.to.brief()))

    def item_link(self, item):
        return u"/data/entry/%s" % item.pk


class CategoryFeed(Feed):
    title = "Denigma Data Categories"
    description = "Catories of Denigma's data entries."
    link = "/data/category/feed/"

    def items(self):
        return Category.objects.all()

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item.definition.brief()

    def item_link(self, item):
        return u"/data/category/%s" % item.pk