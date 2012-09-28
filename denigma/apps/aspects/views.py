from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Hierarchy, HierarchyType, Rank, Grade, Title

from blog.models import Post


def index(request):
    hierarchytypes = HierarchyType.objects.all()
    return render_to_response('aspects/index.html', {'hierarchytypes': hierarchytypes},
        context_instance=RequestContext(request))

def aspect(request, aspect):
    post = Post.objects.get(title=aspect)
    return render_to_response('aspects/aspect.html', {'aspect': aspect},
        context_instance=RequestContext(request))

def research(request):
    pass

def programming(request):
    aspect = Post.objects.get(title='Programming')
    return render_to_response('aspects/aspect.html', {'aspect': aspect},
        context_instance=RequestContext(request))

def design(request):
    pass

def ranks(request):
    hierarchy = Rank.objects.all()
    ctx = {'hierarchy_name': 'Ranks', 'hierarchy': hierarchy}
    return render_to_response('aspects/hierarchy.html', ctx,
        context_instance=RequestContext(request))

def rank(request, name):
    level = Rank.objects.get(name=name)
    return render_to_response('aspects/level.html', {'level': level},
        context_instance=RequestContext(request))

def grades(request):
    hierarchy = Grade.objects.all()
    return render_to_response('aspects/hierarchy.html', {'hierarchy': hierarchy},
        context_instance=RequestContext(request))

def grade(request, name):
    level = Grade.objects.get(name=name)
    return render_to_response('aspects/level.html', {'level': level},
        context_instance=RequestContext(request))

def titles(request):
    hierarchy = Title.objects.all()
    return render_to_response('aspects/hierarchy.html', {'hierarchy': hierarchy},
        context_instance=RequestContext(request))

def title(request, name):
    level = Title.objects.get(name=name)
    return render_to_response('aspects/level.html', {'level': level},
        context_instance=RequestContext(request))

