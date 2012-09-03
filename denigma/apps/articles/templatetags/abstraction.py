"""Template tags to retrieve and manipulate abstracts from articles."""
import re

from django import template


register = template.Library()

@register.filter
def abstract(value):
    """Gets the abstract of a article."""
    if value.startswith("reStructured"):
       return value.replace('\r', '').split('Abstract\n========\n\n')[1].replace('==', '').split('\n')[0]

    paragraphs = value.replace('Abstract', '').replace('==', '').replace('## ', '').replace('--', '').replace('=', '').replace('\r', '').split('\n')
    for paragraph in paragraphs:
        if paragraph and paragraph != "-":
             break
    return paragraph

