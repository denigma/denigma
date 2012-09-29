from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Hierarchy, HierarchyType, Rank, Grade, Title

from blog.models import Post


def index(request):
    aspects = Post.objects.filter(tags__name="aspect")
    aspects_entry = Post.objects.get(title="Aspects")
    print len(aspects)
    hierarchytypes = HierarchyType.objects.all()
    ctx =  {'aspects_entry': aspects_entry,
            'aspects': aspects,
            'hierarchytypes': hierarchytypes}
    return render_to_response('aspects/index.html', ctx,
        context_instance=RequestContext(request))

def aspect(request, aspect):
    aspect = Post.objects.get(title=aspect)
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

def professions(request):
    professions_entry = Post.objects.get(title="Professions")
    professions = Post.objects.filter(tags__name="profession")
    ctx = {'professions_entry': professions_entry, 'professions': professions}
    return render_to_response('aspects/professions.html', ctx,
        context_instance=RequestContext(request))

def profession(request, name):
    print name.title()
    profession = Post.objects.get(title=name.title())
    ctx = {'profession': profession}
    return render_to_response('aspects/profession.html', ctx,
        context_instance=RequestContext(request))

def achievements(request):
    entry = Post.objects.get(title='Achievements')
    #achievements = Post.objects.filter(tags_name='achievement')
    achievements = HierarchyType.objects.all()
    ctx = {'entry': entry, 'achievements': achievements}
    return render_to_response('aspects/achievements.html', ctx, #achievements
        context_instance=RequestContext(request))

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
    ctx = {'hierarchy_name': 'Grades', 'hierarchy': hierarchy}
    return render_to_response('aspects/hierarchy.html', ctx,
        context_instance=RequestContext(request))

def grade(request, name):
    level = Grade.objects.get(name=name)
    return render_to_response('aspects/level.html', {'level': level},
        context_instance=RequestContext(request))

def titles(request):
    hierarchy = Title.objects.all()
    ctx = {'hierarchy_name': 'Titles', 'hierarchy': hierarchy}
    return render_to_response('aspects/hierarchy.html', ctx,
        context_instance=RequestContext(request))

def title(request, name):
    level = Title.objects.get(name=name)
    return render_to_response('aspects/level.html', {'level': level},
        context_instance=RequestContext(request))


