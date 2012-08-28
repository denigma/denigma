from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Post


def index(request):
    tutorials = Post.objects.filter(tags__name='tutorial').order_by('id')
    return render_to_response('tutorials/index.html', {'tutorials': tutorials},
                              context_instance=RequestContext(request))


