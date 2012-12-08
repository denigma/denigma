import re

from django import template


hyperlink = re.compile("(https*://.+?)[;\]]")
register = template.Library()

@register.filter
def hyper(value):
    return hyperlink.sub(r"<a href='\1'>\1</a>]", value).replace('] <', '; <')

