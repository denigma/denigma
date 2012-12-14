import django_tables2 as tables

from models import Interaction
from templatetags.ncbi import geneid, pubmeds


class InteractionTable(tables.Table):

    def render_id_a(self, record, value):
        return geneid(value)

    def render_id_b(self, record, value):
        return geneid(value)

    def render_pmid(self, record, value):
        return pubmeds(value)

    class Meta:
        model = Interaction
        attrs = {'class': 'paleblue'}
        exclude = ('id',)