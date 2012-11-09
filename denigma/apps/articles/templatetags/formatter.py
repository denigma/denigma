# -.- coding: utf8 -.-
"""Formats an article."""
from datetime import datetime

from django import template


register = template.Library()

@register.filter
def footer(text, insert="###Page###"):
    """Inserts a a footer into a text, which is by default a page count."""
    return text + "\n.. footer:: " + insert + "\n"

@register.filter
def header(text, insert=datetime.now):
    """Inserts a header into a text, by default inserts the current time"""
    return text + "\n.. header:: " + insert + "\n"

@register.filter
def link(name, url=None):
    """Generates an rst external link by passing in a name and a url."""
    if not url:
        url = 'http://denigma.de/articles/' + name
    return  "`%s`_\n\n.. _`%s`: %s" % (name, name, url)