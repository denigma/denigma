import datetime
from haystack import indexes
from models import Poll, Choice


class PollIndex(indexes.SearchIndex, indexes.Indexable):
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Poll

    def index_queryset(self):
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())


class ChoiceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Choice

    def index_queryset(self):
        return self.get_model().objects.all()
