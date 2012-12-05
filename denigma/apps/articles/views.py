# -.- coding: utf8 -.-
import os
import re

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from data.models import Entry, Change

from manager import referencing
from templatetags.presenter import present
from templatetags.formatter import header, footer, link, coverPage, pageBreak, tablesAndFigures, glossary
from templatetags.tabling import tables
from templatetags.figuring import figures
from templatetags.math import formula
from templatetags.latinum import latin

try:
    import article as a
except ImportError as e:
    print("No article module available. %s" % e)

try:
    import denigma.library as library #denigma.library as
except ImportError:
    print("No library available.")


def view(request, title):
    """Viewing article by title."""
    article = Entry.objects.get(title=title.replace('_', ' ')) # Deslugify.
    changes = Change.objects.filter(of=article).order_by('-at')
    ctx = {'article': article, 'changes':changes}
    print("Word count = %s" % len(article.text.split(None)))
    return render_to_response('articles/view.html', ctx,
        context_instance=RequestContext(request))


def reference(request, slug, numbered=False):
    article = Entry.objects.get(slug=slug)
    article.text = footer(header(article.text+'\n', link(article.title, "http://denigma.de"+article.get_absolute_url())))
    article.text = referencing(article, linking=True, numbered=numbered)
    #article.text = glossary(article.text)
    print("Word count = %s" % len(article.text.split(None)))
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


def connect(request, slug, references=True):
    """Takes an data entry that collectively connects other data entries.
    Can be used to produce for instance to produce a thesis or a book."""
    connector = Entry.objects.get(slug=slug)

    # Sets the footer and header:
    connector.text = footer(header(connector.text+'\n', link(connector.title, "http://denigma.de"+connector.get_absolute_url())))

    # Gets the cover Page right depending on html or pdf output:
    connector.text = connector.text.replace('\r', '').replace("| ", "\n.. class:: center\n\n ")
    connector.text = coverPage(connector.text)
    connector.text = pageBreak(connector.text)
    #connector.text = connector.text.replace('=', '#')

    rc = re.compile(r'=*\nTable of Contents\n={17,}\n{1,2}.+?\n\n', re.DOTALL)#
    #re.sub()

    parts = []
    global parts

    def translate(match):
        contents = match.group(0) #.split('\n'))
        #print contents
        rc = re.compile('\d\.\s(.+)') #')
        contents = re.findall(rc, contents)

        for content in contents:
            parts.append(Entry.objects.get(title=content))
            #print content
        return "\n.. contents:: **Contents**\n\n"
    connector.text = re.sub(rc, translate, connector.text)


    start_sections = '\n\n.. raw:: pdf\n\n    SetPageCounter 1 arabic\n\n'
    connect_sections = "\n\n.. raw:: pdf\n\n    PageBreak oneColumn\n\n"
    connector.text += start_sections+connect_sections.join([part.text.replace('.. contents:: ', '.. ').replace('.. footer:: ', '.. ')for part in parts]) # tables(formula())

    #connector.text += '\n'+"\n\n.. raw:: pdf\n\n    PageBreak oneColumn\n\n".join([tables(formula(part.text.replace('.. contents:: ', '.. ').replace('.. footer:: ', '.. '))) for part in parts])
    #connector.text = connector.text.encode('ascii', 'ignore')
    # Formatting numbers and tables:
    connector.text = latin(connector.text)#tables()#, uni=False)) formula
    connector.text = formula(connector.text)#, uni=False)
    connector.text = tables(connector.text)
    connector.text = figures(connector.text)
    #connector.text = referencing(connector, linking=False, tables=False)

    #print(connector.text)

    if references:
    # Collecting references:
        article = a.Article()
        references_regex = re.compile("References\n\W{10}(.+?)\n{3}", re.DOTALL)

        #references_regex.sub(translate, references_regex)

        if "References\n==========" in connector.text:
            references = "\n\n".join(re.findall(references_regex, connector.text)).replace('*' , '') # Removes markup.
            article.bibliography = library.Bibliography()
            article.references = a.References(references, article=article)
            paragraph = a.Paragraph(connector.text)
        article.paragraphs = [paragraph]
        article.referencing(numbered=False, brackets=False, connect=True)
        #article.glossaring()
        connector.text = article.__unicode__()
        #print connector.text
        connector.text = tablesAndFigures(connector.text)
        connector.text = glossary(connector.text)

    output = open(os.path.join(settings.PROJECT_ROOT, 'documents', connector.slug+'.rst'), 'w')
    output.write(connector.text.encode('utf8'))
    #output.write(connector.text.encode('utf8'))
    output.close()
    print("Word count = %s" % len(connector.text.split(None)))
    connector.text = connector.text.replace(".. class:: center\n\n", "| ")#.replace(".. raw:: pdf", '..')
    return render_to_response('articles/connected.html', {'article': connector},
        context_instance=RequestContext(request))
