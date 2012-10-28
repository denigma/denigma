"""Template tags to retrieve and manipulate abstracts from articles."""
import re

from django import template


register = template.Library()

@register.filter
def abstract(value):
    """Gets the abstract of a article."""
#    if not isinstance(value, (unicode, str)):
#        return value.text
#    else:
    if ":Abstract:" in value:
        return value.replace('\r', '').split(':Abstract:')[1].split('\n')[0]
    elif "Abstract" in value:
       return value.replace('\r', '').split('Abstract\n========\n\n')[1].replace('==', '').split('\n')[0]
    else:
        return value[:150]


    paragraphs = value.replace('Abstract', '').replace('==', '').replace('## ', '').replace('--', '').replace('=', '').replace('\r', '').split('\n')
    for paragraph in paragraphs:
        if paragraph and paragraph != "-":
             break
    return paragraph

def reST(value):
    pass

