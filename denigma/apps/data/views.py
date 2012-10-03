from django.shortcuts import render_to_response
from django.template import RequestContext

from control import get


def index(request):
    return render_to_response('data/index.html', {'entry': get('Data')},
        context_instance=RequestContext(request))
