# -*- coding: utf-8 -*-
"""Provides template tags that makes the use of both markdown and
ReStructured Text compatible."""
import re
from django import template


header1 = re.compile("<p>#(.+)</p>")
header2 = re.compile("<p>##(.+)")
header3 = re.compile("<p>###(.+)")
header4 = re.compile("<p>####(.+)")

#h1 = re.compile("<h1>(.+?)</h1>")
#h2 = re.compile("<h2>(.+?)</h2>")
#h3 = re.compile("<h3>(.+?)</h3>")
#h4 = re.compile("<h4>(.+?)</h4>")

register = template.Library()

@register.filter
def negle(value):
    """Presevers image urls in combination with neglete wrapped around
    restructedtext."""
    print value.replace('<http://', '#~#')\
    .replace('http://', "linkaging")\
    .replace('#~#', '<http://')\
    .replace("  <b><a href='/data/entry/update/", 'StArTcOnTeNt')\
    .replace("'>o</a></b>", 'EnDcOnTeNt')
    return value.replace('<http://', '#~#')\
                .replace('http://', "linkaging")\
                .replace('#~#', '<http://')
                #.replace("<b><a href='/data/entry/update/", '\n\nStArTcOnTeNt')\
                #.replace("'>o</a></b>", 'EnDcOnTeNt')#.replace('src="http://', 'linkimage').
    # Leaving off the src enables urls in [] but disables plain urls.
    # Exchanging of the middle replace by the commented out leads to the opposite effect

@register.filter
def neglete(value):
    """Negletes the from ReStructured Text performed html demarkuping."""
    print list(value)
    value = value.replace('&lt;', '<')\
         .replace('&quot;', '"')\
         .replace('&gt;', '>')\
         .replace('linkaging', 'http://')
         #.replace('\n\nStArTcOnTeNt', "<b><a href='/data/entry/update/", )\
         #.replace('</p>\n<p>StArTcOnTeNt', " <b><a href='/data/entry/update/")\
         #.replace('EnDcOnTeNt', "'>o</a></b>")  #.replace('linkimage', 'src="http://')\
    print(value)
    value = header4.sub(r"<h4>\1</h4>", value)
    value = header3.sub(r"<h3>\1</h3><p>", value)
    value = header2.sub(r"<h2>\1</h2><p>", value)
    value = header1.sub(r"<h1>\1</h1>", value)

    #value = h4.sub(r"<h5>\1</h5>", value)
    #value = h3.sub(r"<h4>\1</h4>", value)
    #value = h2.sub(r"<h3>\1</h3>", value)
    #value = h1.sub(r"<h2>\1</h2>", value)

    return value
