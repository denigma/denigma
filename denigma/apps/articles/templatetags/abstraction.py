"""Template tags to retrieve and manipulate abstracts from articles."""
import re

from django import template


register = template.Library()

@register.filter
def abstract(value):
    """Gets the abstract of a article."""
    paragraphs = value.replace('Abstract', '').replace('--', '').replace('=', '').replace('\r', '').split('\n')
    for paragraph in paragraphs:
        if paragraph and paragraph != "-":
             break
    return paragraph
