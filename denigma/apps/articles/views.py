from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from data.models import Entry

from manager import referencing
from templatetags.presenter import present


def view(request, title):
    """Viewing article by title."""
    article = Entry.objects.get(title=title.replace('_', ' ')) # Deslugify.
    return render_to_response('articles/view.html', {'article': article},
        context_instance=RequestContext(request))


def reference(request, slug):
    article = Entry.objects.get(slug=slug)
    article.text = referencing(article)
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