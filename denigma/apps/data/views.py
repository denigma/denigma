from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


import reversion

from meta.view import log
from control import get

from models import Entry, Change, Relation
from forms import EntryForm, RelationForm


def index(request):
    return render_to_response('data/index.html', {'entry': get('Data')},
        context_instance=RequestContext(request))

def hierarchy(request, template_name='data/hierarchy.html'):
    ctx =  {'entries': Entry.objects.filter(published=True)}
    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))

def entries(request): pass
def entry(): pass
def add_entry(): pass
def edit_entry(): pass
def remove_entry(): pass

def changes(request, pk=None, template_name='data/change_list.html'):
    if pk:
        print("pk = %s" % pk)
        query = Entry.objects.get(pk=int(pk))
        queryset = Change.objects.filter(of=query).order_by('-at')
        #queryset = query.updates.all()#.order_by('-created')
    else:
        queryset = Change.objects.filter(of__published=True).order_by('-at')
    ctx = {'object_list': queryset, 'object': query}
    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))

def remove_change(request, slug):
    print("remove_change: slug = %s" % slug)
    change = Change.objects.get(slug=slug)
    change.delete()
    msg = 'Successfully removed change %s' % change.title
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/data/changes/%s' % change.of.pk)

def change(request, slug, template_name='data/change.html'):
    print("data.views.change: slug = %s" % slug)
    change = Change.objects.get(slug=slug)
    changes = change.differences()
    print "Change:", change
    print "Changes:", changes.title

    ctx = {'change': change, 'changes': changes}

    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))

def relations(): pass
def relation(): pass
def add_relation(): pass
def edit_relation(): pass
def remove_relation(): pass

def alterations(): pass
def alteration(): pass

def tags(): pass

def tag(request, slug):
    return redirect('/blog/tag/%s' % slug)

def categories(): pass
def category(): pass


class EntryList(ListView):
    queryset=Entry.objects.filter(published=True).order_by('-created')


class ChangeList(ListView): # Not functional.
    def dispatch(self, *args, **kwargs):
        return render_to_response('data/change_list.html')

class Create(CreateView):
    model = Entry
    form_class = EntryForm
    comment = 'Created entry.'
    message = 'Successfully created %s'

    def post(self, request):
        self.request = request
        super(Create, self).post(request)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class Update(UpdateView):
    model = Entry
    form_class = EntryForm
    comment = 'Updated entry'
    message= 'Successfully updated %s'

    def post(self, request, pk):
        self.request = request
        super(Update, self).post(request, pk)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class EntryCreate(Create):
    model = Entry
    form_class = EntryForm
    comment = 'Created entry.'


class EntryUpdate(Update):
    model = Entry
    form_class = EntryForm
    comment = 'Updated Entry'


class RelationCreate(Create):
    model = Relation
    form_class = RelationForm
    comment = 'Created relation.'


class RelationUpdate(Update):
    model = Relation
    form_class = RelationForm
    comment = 'Updated relation'


