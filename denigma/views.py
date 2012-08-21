"""Main view module.
A view is just a Python function that takes an HttpRequest as its parameter
and returns an instance of HttpResponse.
"""
import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext


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
    return render_to_response('meta.html', {'values':sorted(request.META.items())},
                              context_instance=RequestContext(request))

def current_datetime(request):
##    now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
##    t = get_template('current_datetime.html')#"<html><body>It is now {{ current_date }}.</body></html>"
##    html = t.render(Context({'current_date':now}))
##    return HttpResponse(html)
##    return render_to_response('current_datetime.html', {'current_date':now} )
    current_date = datetime.datetime.now()
    return render_to_response('dateapp/current_datetime.html', locals(),
                              context_instance=RequestContext(request))

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    print dt
    #assert False
##    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
##    return HttpResponse(html)
    return render_to_response('dateapp/hours_ahead.html', locals(),
                             context_instance=RequestContext(request))

def google(request):
    render_to_response('google.html', locals())
