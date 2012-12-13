from django.utils.safestring import mark_safe

import django_tables2 as tables

from models import Tissue


class TissueTable(tables.Table):

    def render_name(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    #def render_description(self, record, value):
    #    return mark_safe('<a href="%s">%s</a>' % (record.get_update_url(), value))

    class Meta:
        model = Tissue
        attrs = {"class": "paleblue"}
        fields = ('name', 'description', 'synonyms')