import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def pubmed_links(value):
    rc = re.compile('(?P<pre>[\[\;\s])(?P<id>[1-9]\d{6,})(?P<post>[\]\;\s])')
    def translate(match): #http://www.ncbi.nlm.nih.gov/pubmed/
        return '%s<a href="/datasets/reference/%s">%s</a>%s' % \
               (match.group('pre'), match.group('id'), match.group('id'), match.group('post'))
    return mark_safe(rc.sub(translate, value))
