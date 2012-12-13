from django.utils.safestring import mark_safe

import django_tables2 as tables

from models import Entry

from blog.templatetags.hyperlink import hyper
from blog.templatetags.crosslink import recross


class EntryTable(tables.Table):
    def render_title(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_text(self, record, value):
        #return mark_safe(record.brief())
        return mark_safe(hyper(recross(record.brief())))

    def render_creator(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (value.get_absolute_url(), value))

    class Meta:
        model = Entry
        attrs = {"class": "paleblue"}
        fields = ('title', 'text', 'creator', 'created', 'updated')