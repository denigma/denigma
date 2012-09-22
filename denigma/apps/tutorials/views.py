from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Post


def index(request):
    tutorials_entry = Post.objects.get(title="Tutorials")
    tutorials = Post.objects.filter(tags__name='tutorial').order_by('id')
    ctx = {'tutorial_entry': tutorials_entry, 'tutorials': tutorials}
    return render_to_response('tutorials/index.html', ctx,
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

def development(request):
    """Operation-specific developments considerations."""
    windows = Post.objects.get(title="Windows")
    mac = Post.objects.get(title="Mac")
    linux = Post.objects.get(title="Linux")
    ctx = {'windows': windows, 'mac': mac, 'linux': linux}
    return render_to_response('tutorials/development.html', ctx,
                              context_instance=RequestContext(request))