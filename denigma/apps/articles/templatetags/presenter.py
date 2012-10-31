"""Converts all section to the same level."""
import re
from django import template


register = template.Library()

@register.filter
def present(value):
    value = value.replace('\r', '')\
    .replace('Methods\n=======', '')\
    .replace('Tables & Figures\n================', '')\
    .replace('Tables', '')\
    .replace('.. image: ', '.. image:: ')\
    .replace('\n\n======\n\n', '')\
    .replace('Table 1: ', '')\
    .replace('.. header: ', '.. header:: ')
    print("apps.articles.templatetags.presenter.present: Tables in value = %s" % ('Tables' in value))
    rc = re.compile('(-{3,}|~{3,})')
    def translate(match):
        string = match.group(0)
        length = len(string)
        return "=" * length
    return rc.sub(translate, value)