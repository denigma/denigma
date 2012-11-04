import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def pubmed_links(value):
    rc = re.compile('\d{9,}')
    def translate(match):
        return "<a href=http://www.ncbi.nlm.nih.gov/pubmed/%s>%s</a>" % (match.group(0), match.group(0))
    return mark_safe(rc.sub(translate, value))
