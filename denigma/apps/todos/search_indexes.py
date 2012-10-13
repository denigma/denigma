import datetime

from haystack import indexes

from models import Todo


class TodoIndex(indexes.SearchIndex, indexes.Indexable):
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')
    #start_date = indexes.DateTimeField(model_attr='start_date')
    #stop_date = indexes.DateTimeField(model_attr='stop_date')
    # haystack.exceptions.SearchFieldError: The model '<Todo: PyOpenGL>' has an empty model_attr 'stop_date' and doesn't allow a default or null value.


    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Todo

    def index_queryset(self):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())