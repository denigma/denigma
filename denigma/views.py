"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
from django.shortcuts import render_to_response
from django.http import HttpResponse


def root(request):
    """The root source of all Denigmas URLs."""
    return render_to_response('root.html', locals())

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def meta(request):
    return render_to_response('meta.html', {'values':sorted(request.META.items())})

