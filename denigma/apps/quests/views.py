from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import ugettext as _
from django.db.models import Q


from data.models import Entry, Category, Relation
from data.views import Create
from todos.models import Todo

#from taggit.models import Tag

import reversion

from meta.view import log


def index(request):
    print("quests.index")
    entries = Entry.objects.filter(Q(parent__title="Quests") | Q(categories__name="Quest"))
    quests = Entry.objects.get(title="Quests")
    return render(request, 'quests/index.html',
        {'entries': entries, 'quests': quests})


class CreateQuest(Create):

    def dispatch(self, request, *args, **kwargs):
        self.todo = Todo.objects.get(pk=kwargs['pk'])
        return super(CreateQuest, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(CreateQuest, self).get_initial()
        initial = initial.copy()
        initial['title'] = self.todo.title
        initial['text'] = self.todo.description
        initial['categories'] = Category.objects.filter(name='Quest')
        #initial['tags'] = ['todo']
        return initial


class EngageQuest(Create):

    def dispatch(self, request, *args, **kwargs):
        self.quest = Entry.objects.get(slug=kwargs['slug'])
        del kwargs['slug']
        return super(EngageQuest, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(EngageQuest, self).get_initial()
        initial = initial.copy()
        #initial['title'] = 'engaged'
        initial['parent'] = self.quest
        #tag = Tag.objects.get_or_create(name='questing')
        #initial['tags'] = self.quest.tags.all()#[tag]
        return initial

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username='Anonymous')
            self.object.user = self.request.user
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment, 1)
            comment = self.request.POST['comment'] or "Engaged quest"
            relation = Relation(fr=self.quest, to=self.object, be=Entry.objects.get(title='solved by'))
            relation.user = self.request.user
            relation.save()
            log(self.request, relation, comment, 1)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())




