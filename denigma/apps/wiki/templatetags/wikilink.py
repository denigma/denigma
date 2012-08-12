from django import template
import re

wikilink = re.compile("\\b([A-Z][a-z]+[A-Z][a-z]+)\\b")
register = template.Library()

@register.filter
def wikify(value):
    return wikilink.sub(r"<a href='/wiki/page/\1/'>\1</a>", value)
    
