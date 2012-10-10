import django_tables2 as tables
from django.utils.safestring import mark_safe

from models import Transcript, Replicate

from lifespan.models import Factor


class TranscriptTable(tables.Table):

    def render_symbol(self, value, record):
        try:
            factor = Factor.objects.get(symbol=value)
            value = mark_safe('<a href="/lifespan/factor/%s/">%s</a> %' % (factor.pk, value))
            print value
        except Factor.DoesNotExist:
            pass
        except:
            pass
        return value

    def render_seq_id(self, value, record):
        return mark_safe('<a href="http://flybase.org/reports/%s.html">%s</a>' % (value, value))

    class Meta:
        model = Transcript
        attrs = {'class': 'paleblue'}
        exclude = ('id', 'profile')


class ReplicateTable(tables.Table):
    class Meta:
        model = Replicate
        attrs = {'class': 'paleblue'}
        exclude = ('id',)


class AnnotationTable(tables.Table):
    categoryName = tables.Column()
    termName = tables.Column()
    listHits = tables.Column()
    percent = tables.Column()
    ease = tables.Column()
    #genes = tables.Column()
    listTotals = tables.Column()
    foldEnrichment = tables.Column()
    bonferroni = tables.Column()
    benjamini = tables.Column()
    FDR = tables.Column()

    class Meta:
        attrs = {'class': 'paleblue'}