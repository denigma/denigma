from haystack import indexes
from models import Classification, Tissue, Species


class ClassificationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Classification

    def index_queryset(self):
        return self.get_model().objects.all()


class TissueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tissue

    def index_queryset(self):
        return self.get_model().objects.all()


class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Species

    def index_queryseq(self):
        return self.get_model().objects.all()
