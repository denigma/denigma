import datetime

from haystack import indexes

from models import Entry, Change, Category, Relation, Alteration


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')

    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()
    categories = indexes.MultiValueField()

    def get_model(self):
        return Entry

    def index_queryset(self):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now(), published=True)


class ChangeIndex(indexes.SearchIndex, indexes.Indexable):
    at = indexes.DateTimeField(model_attr='at')

    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()
    categories = indexes.MultiValueField()

    def get_model(self):
        return Change

    def index_queryset(self):
        return self.get_model().objects.filter(at__lte=datetime.datetime.now(), of__published=True)


class RelationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Relation

    def index_queryset(self):
        return self.get_model().objects.all()


class AlterationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Alteration

    def index_queryset(self):
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Category

    def index_queryset(self):
        return self.get_model().objects.all()