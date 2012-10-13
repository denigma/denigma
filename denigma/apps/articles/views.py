from django.shortcuts import render_to_response
from django.template import RequestContext

from data.models import Entry


def view(request, title):
    """Viewing article by title."""
    article = Entry.objects.get(title=title.replace('_', ' ')) # Deslugify.
    return render_to_response('articles/view.html', {'article': article},
                              context_instance=RequestContext(request))
