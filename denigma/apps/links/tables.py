
from django.utils.safestring import mark_safe

from django_tables2 import Table

from data.templatetags.paragraphs import firstpara

from models import Link
from templatetags.contacting import contact


class LinkTable(Table):
    def render_url(self, record, value):
        return mark_safe('<a href="%s">|Link|</a>' % value)

    def render_title(self, record, value):
        return mark_safe('<a href="%s">%s' % (record.get_absolute_url(), value))

    def render_description(self, value, record):
        return mark_safe('%s <a href="/links/update/%s">o</a>' % (firstpara(value), record.id))

    def render_contact(self, record, value):
        return mark_safe(contact(value))

    class Meta:
        model = Link
        attrs = {"class": "paleblue"}
        fields = ('title', 'url', 'description', 'creation')
        exclude = ('id', 'language', 'visibility', 'ordering',
                   'publication_start', 'publication_end', 'site', 'tags', 'contact')

