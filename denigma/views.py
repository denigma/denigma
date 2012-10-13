"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from data import get
from data.models import Entry
from blog.models import Post

from django import forms


class SearchForm(forms.Form):
   text = forms.CharField(label="")#label="Site-wide search")


def home(request):
    """The root source of all Denigmas URLs.
    Renders a dynamic home site with altered content."""
    searchform = SearchForm() # Depricated?
    denigma_description = get("Denigma Description")
    denigma_rationality = get("Denigma Rationality")
    news = Entry.objects.filter(tags__name='news').order_by('-created', '-id')[:8]\
        or Post.objects.filter(tags__name='news').order_by('-created', '-id')[:8]
    research = get("Research")
    programming = get("Programming")
    design = get("Design")
    dashboard = get("Dashboard")
    ctx = {'searchform': searchform,
           'denigma_description': denigma_description,
           'denigma_rationality': denigma_rationality,
           'news': news,
           'dashboard':dashboard,
           'research': research,
           'programming': programming,
           'design': design}
    return render_to_response('homepage.html', ctx,
                              context_instance=RequestContext(request))

def search(request, term):
    """Site-wide search functionality"""
    term = request.META['QUERY_STRING'].split('models=data&q=')[1]
    return render_to_response('search.html', {'term': term},
        context_instance=RequestContext(request))

def google(request, term):
    return render_to_response('google.html', term)

def content(request):
    contents = get('Content'), get("Data App"), get("Denigma Blog"), get("Danigma's Wiki")
    return render_to_response('content.html', {'contents': contents},
        context_instance=RequestContext(request))