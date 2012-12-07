import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def pubmed_links(value):
    rc = re.compile('\W(?P<id>[1-9]\d{6,})\W')
    def translate(match):
        return "<a href=http://www.ncbi.nlm.nih.gov/pubmed/%s>%s</a>" % (match.group(0), match.group(0))
    return mark_safe(rc.sub(translate, value))
