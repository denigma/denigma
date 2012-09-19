from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response('chrono/index.html', context_instance=RequestContext(request))

def gettime(request):
    if request.is_ajax():
        return HttpResponse(str(datetime.now()))

    # Graceful degradation
    return render_to_response('chrono/index.html', {'time': str(datetime.now())}, context_instance=RequestContext(request))

def current_datetime(request):
##    now = datetime.datetime.now()
#html = "<html><body>It is now %s.</body></html>" % now
##    t = get_template('current_datetime.html')#"<html><body>It is now {{ current_date }}.</body></html>"
##    html = t.render(Context({'current_date':now}))
##    return HttpResponse(html)
##    return render_to_response('current_datetime.html', {'current_date':now} )
    current_date = datetime.now()
    return render_to_response('chrono/current_datetime.html', locals(),
        context_instance=RequestContext(request))

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.now() + timedelta(hours=offset)
    print dt
    #assert False
    ##    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    ##    return HttpResponse(html)
    return render_to_response('chrono/hours_ahead.html', locals(),
        context_instance=RequestContext(request))