from haystack import indexes

from models import Signature, Set #Profile,


# No profiles yet:
#class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#
#    def get_model(self):
#        return Profile
#
#    def index_queryset(self):
#        return self.get_model().objects.all()


class SignatureIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Signature

    def index_queryset(self):
        return self.get_model().objects.all()


class SetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Set

    def index_queryset(self):
        return self.get_model().objects.all()