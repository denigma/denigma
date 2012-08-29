from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Post


def index(request):
    tutorials = Post.objects.filter(tags__name='tutorial').order_by('id')
    return render_to_response('tutorials/index.html', {'tutorials': tutorials},
                              context_instance=RequestContext(request))

def view(request, tutorial_id):
    print "Tutorial id is:", tutorial_id, type(tutorial_id)
    tutorial = Post.objects.get(pk=tutorial_id)
    return render_to_response("./tutorials/view.html", {'tutorial': tutorial},
                              context_instance=RequestContext(request, {}))

def edit(request, tutorial_id):
    tutiorial = Post.object.get(pk=tutorial_id)
    return render_to_response("./tutorials/view.html", {'tutorial': tutorial},
                             context_instance=RequestContext(request, {}))
