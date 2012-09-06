import datetime
from haystack import indexes
from models import Page, Tag


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()

    def get_model(self):
       return Page

    def index_queryset(self):
       return self.get_model().objects.all()


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tag

    def index_queryset(self):
        return self.get_model().objects.all()
