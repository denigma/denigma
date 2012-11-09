# -.- coding: utf8 -.-
import os
import re

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from data.models import Entry, Change

from manager import referencing
from templatetags.presenter import present
from templatetags.formatter import header, footer, link


def view(request, title):
    """Viewing article by title."""
    article = Entry.objects.get(title=title.replace('_', ' ')) # Deslugify.
    changes = Change.objects.filter(of=article).order_by('-at')
    ctx = {'article': article, 'changes':changes}
    return render_to_response('articles/view.html', ctx,
        context_instance=RequestContext(request))


def reference(request, slug):
    article = Entry.objects.get(slug=slug)
    article.text = referencing(article, linking=False)
    return render_to_response('articles/view.html', {'article': article},
        context_instance=RequestContext(request))

def presentation(request, slug):
    article = Entry.objects.get(slug=slug)
    article.text = present(referencing(article))
    output = open('presentation.rst', 'w')
    output.write(article.text)
    output.close()
    return render_to_response('articles/view.html', {'article': article},
        context_instance=RequestContext(request))

def output(request, pk):
    # Write text out into file.
    #name = entry.slug
    # Call rst2pdf name.rst -o name.pdf
    pass


def connect(request, slug):
    """Takes an data entry that collectively connects other data entries.
    Can be used to produce for instance to produce a thesis or a book."""
    connector = Entry.objects.get(slug=slug)

    # Sets the footer and header:
    connector.text = footer(header(connector.text, link(connector.title, connector.get_absolute_url())))

    # Gets the cover Page right depending on html or pdf output:
    connector.text = connector.text.replace('\r', '').replace("| ", "\n.. class:: center\n\n ")

    #connector.text = connector.text.replace('=', '#')

    rc = re.compile(r'=*\nTable of Contents\n={17,}\n{1,2}.+?\n\n', re.DOTALL)#
    #re.sub()

    parts = []
    global parts

    def translate(match):
        contents = match.group(0) #.split('\n'))
        print contents
        rc = re.compile('\d\.\s(.+)') #')
        contents = re.findall(rc, contents)

        for content in contents:
            parts.append(Entry.objects.get(title=content))
            #print content
        return "\n.. contents:: **Contents**\n\n"
    connector.text = re.sub(rc, translate, connector.text)

    connector.text += '\n'+"\n\n.. raw:: pdf\n\n    PageBreak oneColumn\n\n".join(
        [part.text.replace('.. contents:: ', '.. ').replace('.. footer:: ', '.. ') for part in parts])
    #print(connector.text)

    output = open(os.path.join(settings.PROJECT_ROOT, 'documents', connector.slug+'.rst'), 'w')
    output.write(connector.text.encode('utf8'))
    output.close()

    connector.text = connector.text.replace(".. class:: center\n\n", "| ").replace(".. raw:: pdf", 'dsa')
    return render_to_response('articles/view.html', {'article': connector},
        context_instance=RequestContext(request))