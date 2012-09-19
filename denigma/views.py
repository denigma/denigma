"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from blog.models import Post

from django import forms


class SearchForm(forms.Form):
   text = forms.CharField(label="")#label="Site-wide search")


def home(request):
    """The root source of all Denigmas URLs.
    Renders a dynamic home site with altered content."""
    posts = Post.objects.filter(tags__name='news').order_by('-created', '-id')[:8] # Fetches all news.
    searchform = SearchForm()
    return render_to_response('homepage.html', {'posts': posts, 'searchform': searchform},
                              context_instance=RequestContext(request))

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def meta(request):
    return render_to_response('meta.html', {'values':sorted(request.META.items())},
                              context_instance=RequestContext(request))


def google(request, term):
    return render_to_response('google.html', term)

def search(request, term):
    """Site-wide search functionality"""
    term = request.META['QUERY_STRING'].split('models=data&q=')[1]
    return render_to_response('search.html', {'term': term},
                              context_instance=RequestContext(request))
