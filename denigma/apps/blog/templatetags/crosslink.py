"""A diverse set of crossling algorithms to cross-link blog posts witheach other."""

import re

from django import template

from blog.models import Post


register = template.Library()


@register.filter
def cross(text):
    """Performs a crosslinking for single words via dict look-up."""
    posts = tuple([p.title for p in Post.objects.all()])
    terms = text.split(' ')
    for index, term in enumerate(terms):
       if term in posts:
          post = Post.objects.get(title=term)
          terms[index] = '<a href="/blog/{0}">{1}</a>'.format(post.id, term)
    text = " ".join(terms)
    return text


@register.filter
def crossing(text):
    """Most powerful crosslinking by utilizing regular expression matching.
    So far the regex only replaces single words."""
    posts = dict([(p.title, '<a href="/blog/{0}">{1}</a>'.format(p.id, p.title))\
            for p in Post.objects.all()])

    def replace(text):
        print text.group(0)
        return posts.get(text.group(0), text.group(0))

    print posts
    text = re.sub(r'[\w\d]+', replace, text)
    return text
   

@register.filter
def crossed(text):
    """Simple crosslinking replace algorithms, which might not work perfectly."""
    posts = dict([(p.title, '<a href="/blog/{0}">{1}</a>'.format(p.id, p.title))\
            for p in Post.objects.all()])
    for title in posts:
        text = text.replace(title, posts[title])
    return text

@register.filter
def recross(text):
    """Takes a text and replaces words that match a key in the posts dictionary with
    the assoicated cross-linked value, return the changed text.""" 
    posts = dict([(p.title, '<a href="/blog/{0}">{1}</a>'.format(p.id, p.title))\
            for p in Post.objects.all()])
    rc = re.compile('|'.join(map(re.escape, posts)))
    def translate(match):
        return posts[match.group(0)]
    return rc.sub(translate, text)
