"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site
from django import forms

from data import get
from data.models import Entry

from blog.models import Post

from donation.models import Donation



class SearchForm(forms.Form):
   text = forms.CharField(label="") #label="Site-wide search")


def home(request, template='homepage.html'):
    """The root source of all Denigmas URLs.
    Renders a dynamic home site with altered content."""
    searchform = SearchForm() # Depricated?
    denigma_description = get("Denigma Description")
    denigma_rationality = get("Denigma Rationality")
    news = Entry.objects.all().order_by('-created', '-id').distinct()[:8]#.filter(Q(tags__name='news') |
                                #Q(categories__name='News')).order_by('-created', '-id').distinct()[:8]\
     #   or Post.objects.filter(tags__name='news')
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
           'design': design,

           'site': Site.objects.get_current,
           'total': Donation.objects.get_total,
           'donation_name': settings.DONATION_NAME,
           'donation_number': settings.DONATION_NUMBER,
           'paypal_id': settings.PAYPAL_ID,
           'debug': settings.DEBUG,
    }


    return render(request, template, ctx)

def search(request, term, template='search.html'):
    """Site-wide search functionality"""
    term = request.META['QUERY_STRING'].split('models=data&q=')[1]
    return render(request, template, {'term': term})

def google(request, term, template='google.html'):
    return render(request, template, term)

def content(request, template='content.html'):
    contents = get('Content'), get("Data App"), get("Denigma Blog"), get("Denigma's Wiki")
    return render(request, template, {'contents': contents})

def repository(request, template='repository.html'):
    """A biologist-friendly data repository."""
    entry = get('Biology of Aging Repository')

    return render(request, template, {'entry': entry})

