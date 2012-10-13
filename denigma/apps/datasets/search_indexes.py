from haystack import indexes

from models import Reference, Change


class ReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Reference

    def index_queryset(self):
        return self.get_model().objects.all()


class ChangeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Change

    def index_queryset(self):
        return self.get_model().objects.all()