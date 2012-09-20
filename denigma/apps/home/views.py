from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return HttpResponse("Home Page")

def index(request):
    return render_to_response('home/index.html', {'user': request.user})

def base(request):
    return render_to_response('home/base.html',
                             {'user': request.user,
                              'error_msg': request.GET.get('error_msg', ''),
                             }, context_instance=RequestContext(request))

def page(request):
   return render_to_response('home/page.html',
                             context_instance=RequestContext(request))


