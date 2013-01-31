# -*- coding: utf-8 -*-
"""A diverse set of crosslinking algorithms to cross-link blog posts witheach other."""

import re

from django import template
from django.conf import settings
from django.db.models import Q

from data.models import Entry, Relation


register = template.Library()


@register.filter
def cross(text):
    """Performs a crosslinking for single words via dict look-up."""
    posts = tuple([e.title for e in Entry.objects.all()])
    terms = text.split(' ')
    for index, term in enumerate(terms):
       if term in posts:
          entry = Entry.objects.get(title=term)
          terms[index] = '<a href="/blog/{0}">{1}</a>'.format(entry.id, term)
    text = " ".join(terms)
    return text


@register.filter
def crossing(text):
    """Most powerful crosslinking by utilizing regular expression matching.
    So far the regex only replaces single words."""
    entries = dict([(e.title, '<a href="/blog/{0}">{1}</a>'.format(e.id, e.title))\
            for e in Entry.objects.all()])

    def replace(text):
        print text.group(0)
        return entries.get(text.group(0), text.group(0))

    print entries
    text = re.sub(r'[\w\d]+', replace, text)
    return text
   

@register.filter
def crossed(text):
    """Simple cross-linking replace algorithms, which might not work perfectly."""
    entries = dict([(e.title, '<a href="/blog/{0}">{1}</a>'.format(e.id, e.title))\
            for e in Entry.objects.all()])
    for title in entries:
        text = text.replace(title, entries[title])
    return text

@register.filter
def recross(text):
    """Takes a text and replaces words that match a key in the posts dictionary with
    the associated cross-linked value, return the changed text."""
    entries = dict([(e.title, u'<a href="{0}">{1}</a>'.format(e.get_absolute_url(), e.title))\
            for e in Entry.objects.all()])
    if entries: # Check if whether database is non-empty (as it is by setting up).

        # Sorts according to term length (long terms first):
        listed_entries = list(entries)
        listed_entries.sort(key=len)
        listed_entries.reverse()

        rc = re.compile(r'(?P<pre>\W?)(?P<term>%s)(?P<post>\W|s)' % '|'.join(map(re.escape, listed_entries)))
        def translate(match):
            return match.group('pre')+entries[match.group('term')]+match.group('post')
        return rc.sub(translate, text)
    return text

@register.filter
def generate(text):
    rc = re.compile(r'\[\[(?P<title>.+)\]\]')
    def translate(match):
        title = match.group(1)
        if not title.startswith('<'):
            return '<a href="%s/data/entry/generate/%s" style="color: #CC0000">%s</a>' % (settings.BASE_URL, title, title)
        return title
    return rc.sub(translate, text).replace('[[', '').replace(']]', '')


@register.filter
def relate(text):
    rc = re.compile(r'<p>(?P<source>.+)#(?P<type>.+)#(?P<target>.+)</p>')
    def translate(match):
        source, type, target = match.group('source'), match.group('type'), match.group('target')
        source_label, type_label, target_label = source.title().replace('_', ' '), type.replace('_', ' '), target.title().replace('_', ' ')
        try:
            relation = Relation.objects.get(Q(fr__title=source_label) & Q(be__title=type_label) & Q(to__title=target_label))
            return '%s %s %s' % (source_label, type_label, target_label)
        except Exception as e:
            return '<a href="%s/data/relation/generate/%s/%s/%s" style="color: #CC0000">%s %s %s</a>' % \
                (settings.BASE_URL, source, type, target, source, type, target)
    return rc.sub(translate, text)