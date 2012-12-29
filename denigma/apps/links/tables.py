
from django.utils.safestring import mark_safe

from django_tables2 import Table

from models import Link


class LinkTable(Table):
    def render_title(self, record, value):
        return mark_safe('<a href="%s">%s' % (record.url, value))

    def render_description(self, value, record):
        return mark_safe('<a href="/links/update/%s">%s</a>' % (record.id, value))

    def render_contact(self, record, value):
        if value:
            if "@" in value:
                return mark_safe('<a href="mailto:%s">%s</a>' % (value, value.replace('@', '(at)')))
            elif value.startswith('http'):
                return mark_safe('<a href="%s">%s</a>' % (value, value.replace('www.', '').split('://')[-1]))
            elif value.startswith('www.'):
                return mark_safe('<a href="http://%s">%s</a>' % (value, value.split('www.')[-1]))
            else:
                return value
        else:
            return value

    class Meta:
        model = Link
        attrs = {"class": "paleblue"}
        exclude = ('id', 'language', 'visibility', 'ordering', 'url',
                   'publication_start', 'publication_end', 'site', 'tags')

