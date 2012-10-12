
from django.utils.safestring import mark_safe

from django_tables2 import Table

from models import Link


class LinkTable(Table):
    def render_title(self, value, record):
        return mark_safe('<a href="%s">%s' % (record.url, value))

    def render_description(self, value, record):
        return mark_safe('<a href="/links/update/%s">%s</a>' % (record.id, value))

    class Meta:
        model = Link
        attrs = {"class": "paleblue"}
        exclude = ('id', 'language', 'visibility', 'ordering', 'url',
                   'publication_start', 'publication_end', 'site', 'tags')

