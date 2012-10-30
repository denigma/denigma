from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from data.models import Entry

from manager import referencing


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

def output(request, pk):
    # Write text out into file.
    #name = entry.slug
    # Call rst2pdf name.rst -o name.pdf
    pass