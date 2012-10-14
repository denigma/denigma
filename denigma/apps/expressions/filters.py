import django_filters

from models import Transcript


class TranscriptFilterSet(django_filters.FilterSet):
    pvalue = django_filters.NumberFilter(lookup_type='lt') # Looks up transcripts with
    benjamini = django_filters.NumberFilter(lookup_type='lt')
    expression__exp = django_filters.NumberFilter(lookup_type='lt')
    #ctr = django_filters.NumberFilter(lookup_type='lt')
    symbol = django_filters.CharFilter()
    class Meta:
        model = Transcript
        fields = ['symbol', 'expression__exp', 'ratio', 'fold_change']#, 'pvalue']#'ctr',

    def __init___(self, *args, **kwargs):
        super(TranscriptFilterSet, self).__init__(*args, **kwargs)
        self.filters['symbol'].extra.update(
            {'empty_label': u'All Symbol'}
        )