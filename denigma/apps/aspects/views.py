from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import CreateView

from models import Hierarchy, HierarchyType, Rank, Grade, Title
from forms import AchievementForm, HierarchyForm, RankForm, GradeForm, TitleForm


from blog.models import Post


class AchievementCreate(CreateView):
    template_name = 'aspects/achievement_form.html'
    success_url = '/aspects/achievements/'
    form_class = AchievementForm
    model = HierarchyType

#    def dispatch(self, *args, **kwargs):
#        self.kwargs.update(kwargs)
#        return super(AchievementCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AchievementCreate, self).get_context_data(**kwargs)
        context['action'] = 'Create'
#        context.update(kwargs)
        return context


class HierarchyCreate(CreateView):
    form_class = HierarchyForm
    model = Hierarchy
    template_name = 'aspects/hierarchy_form.html'

    def dispatch(self, *args, **kwargs):
        self.name = kwargs['name']
        return super(HierarchyCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(HierarchyCreate, self).get_context_data(*args, **kwargs)
        context['action'] = 'Create'
        context['hierarchy_name'] = self.name[:-1].title()
        HierarchyCreate.success_url = '/aspects/%s/' % self.name
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        print self.object
        return HttpResponseRedirect(self.get_success_url())


class RankCreate(HierarchyCreate):
    form_class = RankForm
    model = Rank
    success_url = '/aspects/research/ranks/'


class GradeCreate(HierarchyCreate):
    form_class = GradeForm
    model = Grade
    success_url = '/aspects/programming/grades/'


class TitleCreate(HierarchyCreate):
    form_class = TitleForm
    model = Title
    success_url = '/aspects/design/titles/'


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
    achievements = HierarchyType.objects.all()[:3]
    ctx = {'entry': entry, 'achievements': achievements}
    return render_to_response('aspects/achievements.html', ctx, #achievements
        context_instance=RequestContext(request))

def add_achievement(request):
    return HttpResponse("Create Achievement: %s" % request)

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


