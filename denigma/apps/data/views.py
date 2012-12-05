from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.views.generic import  ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

import reversion
from taggit.models import Tag, TaggedItem

from meta.view import log
from control import get

from models import Entry, Change, Relation, Category
from forms import EntryForm, RelationForm, CategoryForm, DeleteForm


def graph(request, template='data/graph.html'):
    """View that generates a data graph connecting data entries with relations."""
    network = {
        'dataSchema': {
            'nodes': [
                {'name': 'label', 'type': 'string'},
                {'name': 'text', 'type': 'string'},
                {'name': 'links', 'type': 'string'}
            ],
            'edges': [
                {'name': 'label', 'type': 'string'},
                {'name': 'text', 'type': 'string'},
                {'name': 'links', 'type': 'string'}
            ]
        },
        'data': { # Dummy data:
            'nodes': [
                {'id': '1', 'label': 'Concepts', 'text':'Denigma Concepts'},
                {'id': '2', 'label': 'Aspects', 'text':'Three aspects'}
            ],
            'edges': [
                {'id': '2to1', 'label': 'belongs_to', 'text':'A belonging to relationship', 'target':'1', 'source': '2'}
            ]
        }
    }
    memo = []
    def node(entry):
        "Helper function to construct a node object."
        memo.append(entry.pk)
        return {'id': str(entry.pk), 'label': entry.title, 'text': entry.text,
                'links': '<a href="%s">View</a> | <a href="%s">Update</a>' %
                         (entry.get_absolute_url(), entry.get_update_url())}

    # Getting the actually data:
    data = {'nodes':[], 'edges':[]}
    relations = Relation.objects.all()
    for relation in relations:
        fr = relation.fr
        be = relation.be
        to = relation.to
        if fr.pk not in memo:
            data['nodes'].append(node(fr))
        if to.pk not in memo:
            data['nodes'].append(node(to))
        data['edges'].append({'id': "%sto%s" % (fr.pk, to.pk), 'label': be.title, 'text': be.text,
                              'source': str(fr.pk), 'target': str(to.pk), 'directed': True,
                              'links': '<a href="%s">View</a> | <a href="%s">Update</a>' %
                                       (relation.get_absolute_url(), relation.get_update_url())})
    network['data'] = data

    network_json = simplejson.dumps(network)
    return render(request, template, {'network_json': network_json})

def index(request):
    ctx = {'entry': get('Data App'),
           'hierarchy': get('Data Hierarchy'),
           'categories': get('Data Categories'),
           'tags': get('Data Tags')}
    return render_to_response('data/index.html', ctx,
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

def breadcrump(request, slug):
    print("Breadcrump: %s" % slug)
    entry = Entry.objects.get(slug=slug)
    return render_to_response('entry_view.html', {'entry': entry},
        context_instance=RequestContext(request))

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


class TagDetail(ListView):
    #def fill_context(self):
        #self.request

    def dispatch(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            tag = Tag.objects.get(slug=kwargs['slug'])
        else:
            tag = Tag.objects.get(pk=kwargs['pk'])
        items = TaggedItem.objects.filter(tag__pk=tag.pk)
        for item in items:
            print("Item: %s;" % vars(item))
        ctx = {'object_list': items, 'object': tag}
        return render_to_response('data/tag_detail.html', ctx,
            context_instance=RequestContext(request))


class View(object):
    comment = 'Viewed it.'
    message = 'Viewing'
    action = 'View'

    def post(self, request):
        self.request = request
        super(View, self).post(request)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['action'] = self.action
        return context

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
            log(self.request, self.object, comment)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class Create(CreateView):
    model = Entry
    form_class = EntryForm
    comment = 'Created entry.'
    message = 'Successfully created %s'
    action = 'Create'

    def post(self, request):
        self.request = request
        super(Create, self).post(request)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['action'] = self.action
        return context

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
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class Update(UpdateView):
    model = Entry
    form_class = EntryForm
    comment = 'Updated entry.'
    message = 'Successfully updated %s'
    action = 'Update'

    def post(self, request, *args, **kwargs):
        self.request = request
        super(Update, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['action'] = self.action
        return context

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            print("self.object: %s" % self.object)
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username='Anonymous')
            self.object.user = self.request.user
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment, 2)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class Delete(DeleteView):
    model = Entry
    form_class = DeleteForm
    comment = 'Deleted entry'
    message = 'Successfully deleted %s'
    action = 'Delete'
    success_url = reverse_lazy('list-entries')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Delete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        context['action'] = self.action
        context['form'] = DeleteForm()
        return context

    def post(self, request, *args, **kwargs):
        self.request = request
        super(Delete, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())

    def delete(self, request, *args, **kwargs):
        #print("data.views.Delete.delete()")
        with reversion.create_revision():
            self.object = self.get_object()
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username='Anonymous')
            self.object.user = self.request.user
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.delete()
            log(self.request, self.object, comment, 3)
            reversion.set_user(self.request.user)
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())



class EntryView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        #print("data.views.EntryView.dispatch: args=%s, kwargs=%s" % (args, kwargs))
        if 'slug' in kwargs:
            self.slug = kwargs['slug']
        return super(EntryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        objects = Entry.objects.filter(slug=self.slug)
        return objects

    def get_context_data(self, *args, **kwargs):
        ctx = super(EntryView, self).get_context_data(*args, **kwargs)
        if 'slug' in kwargs:
            ctx['slug'] =  self.slug = self.kwargs['slug']
        return ctx


class EntryCreate(Create):
    comment = 'Created entry.'


class EntryUpdate(Update):
    comment = 'Updated entry'

    def dispatch(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            self.slug = kwargs['slug']
            #del kwargs['slug']
        elif 'pk' in kwargs:
            self.pk = kwargs['pk']
            #del kwargs['pk']
        return super(EntryUpdate, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if hasattr(self, 'slug'):
            objects = Entry.objects.filter(slug=self.slug)
        else:
            objects = Entry.objects.all()#filter(pk=self.pk)
        return objects

class EntryDelete(Delete): pass


class RelationCreate(Create):
    model = Relation
    form_class = RelationForm
    comment = 'Created relation.'


class RelationUpdate(Update):
    model = Relation
    form_class = RelationForm
    comment = 'Updated relation.'


class CategoryCreate(Create):
    model = Category
    form_class = CategoryForm
    comment = 'Created category.'


class CategoryUpdate(Update):
    model = Category
    form_class = CategoryForm
    comment = 'Updated category.'
