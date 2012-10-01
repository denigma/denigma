import django_filters

from models import Transcript


class TranscriptFilterSet(django_filters.FilterSet):
    pvalue = django_filters.NumberFilter(lookup_type='lt') # Looks up transcripts with
    class Meta:
        model = Transcript
        fields = ['symbol']#, 'ratio', 'pvalue']

    def __init___(self, *args, **kwargs):
        super(TranscriptFilterSet, self).__init__(*args, **kwargs)
        self.filters['symbol'].extra.update(
            {'empty_label': u'All Symbol'}
        )