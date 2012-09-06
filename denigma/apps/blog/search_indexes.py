import datetime
from haystack import indexes
from apps.blog.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')

    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()

    def get_model(self):
        return Post

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())
