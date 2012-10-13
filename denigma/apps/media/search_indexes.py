import datetime

from haystack import indexes

from models import Image


class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    uploaded = indexes.DateTimeField(model_attr='uploaded')

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Image

    def index_queryset(self):
        return self.get_model().objects.filter(uploaded__lte=datetime.datetime.now())