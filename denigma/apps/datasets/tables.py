from django.utils.safestring import mark_safe

import django_tables2 as tables

from models import Reference


class ReferenceTable(tables.Table):

    def render_pmid(self, value, record):
        if value != None:
            return mark_safe('<a href="http://www.ncbi.nlm.nih.gov/pubmed/%s">%s</a>' % (value, value))
        else:
            return None

    def render_title(self, value, record):
        return mark_safe('<a href="/datasets/reference/update/%s">%s</a>' % (record.pk, value))

    def render_date(self, value, record):
        return mark_safe('<a href="/admin/datasets/reference/%s">%s</a>' % (record.pk, value))

    def render_authors(self, value, record):
        return mark_safe('<a href=%s>%s</a>' % (record.get_absolute_url(), record.repr()))

    class Meta:
        model = Reference
        attrs = {"class": "paleblue"}
        fields = ('authors', 'title', 'date', 'pmid')# 'citation')
        #include = ('citation'),
        #exclude = ('id', )