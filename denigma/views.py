"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
from django.shortcuts import render_to_response


def root(request):
    """The root source of all Denigmas URLs."""
    return render_to_response('root.html', locals())
