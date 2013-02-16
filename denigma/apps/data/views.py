from random import random

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.views.generic import  ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
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
from add.forms import handlePopAdd
from blog.templatetags.hyperlink import hyper
from blog.templatetags.crosslink import recross

from models import Entry, Change, Relation, Alteration, Category
from forms import EntryForm, RelationForm, CategoryForm, DeleteForm
from tables import EntryTable
from filters import TableFilter, EntryFilterSet, FilterForm
from templatetags.rendering import markdown


def graph(request, template='data/graph.html'):
    """View that generates a data graph connecting data entries with relations."""
    network = {
        'dataSchema': {
            'nodes': [
                {'name': 'label', 'type': 'string'},
                {'name': 'text', 'type': 'string'},
                {'name': 'links', 'type': 'string'},
                {'name': 'weight', 'type': 'number' }
            ],
            'edges': [
                {'name': 'label', 'type': 'string'},
                {'name': 'text', 'type': 'string'},
                {'name': 'links', 'type': 'string'},
                {'name': 'weight', 'type': 'number' }
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
        """Helper function to construct a node object."""
        if entry.pk not in memo:
            memo.append(entry.pk)
            data['nodes'].append({'id': str(entry.pk), 'label': entry.title, 'text': recross(hyper(markdown(entry.text))),
                    'links': '<a href="%s">View</a> | <a href="%s">Update</a>' %
                             (entry.get_absolute_url(), entry.get_update_url()), 'weight':random()})

    # Getting the actually data:
    data = {'nodes':[], 'edges':[]}
    relations = Relation.objects.all()
    for relation in relations:
        fr = relation.fr
        be = relation.be
        to = relation.to
        node(fr)
        node(to)
        data['edges'].append({'id': "%sto%s" % (fr.pk, to.pk), 'label': be.title, 'text': markdown(be.text),
                              'source': str(fr.pk), 'target': str(to.pk), 'directed': True,
                              'links': '<a href="%s">View</a> | <a href="%s">Update</a>' %
                                       (relation.get_absolute_url(), relation.get_update_url()), 'weight':random()})
    network['data'] = data

    network_json = simplejson.dumps(network)
    return render(request, template, {'network_json': network_json})


def vivagraph(request, pk=None, template='data/vivagraph/graph2.html'):
    graph = {
        "nodes":[{"name":"Myriel","group":1},
                 {"name":"Napoleon","group":1}
        ],
        "links":[{"source":1,"target":0,"value":1},
                 {"source":2,"target":0,"value":8}
        ]
    }
    graph = {'nodes':[], 'links':[]}
    memo = []

    def node(entry):
        if entry.pk not in memo:
            memo.append(entry.pk)
            graph['nodes'].append({'name': entry.title, 'group':1, 'text': entry.text}) #'image'=

    rels = Relation.objects.all()
    for relation in rels:
        fr = relation.fr
        be = relation.be
        to = relation.to
        node(fr)
        node(to)
        graph['links'].append({'source': fr.title, 'target': to.title, 'value': {'title': be.title, 'text': be.text}})
    #graph = {"nodes":[{"name":"Myriel","group":1},{"name":"Napoleon","group":1},{"name":"Mlle.Baptistine","group":1},{"name":"Mme.Magloire","group":1},{"name":"CountessdeLo","group":1},{"name":"Geborand","group":1},{"name":"Champtercier","group":1},{"name":"Cravatte","group":1},{"name":"Count","group":1},{"name":"OldMan","group":1},{"name":"Labarre","group":2},{"name":"Valjean","group":2},{"name":"Marguerite","group":3},{"name":"Mme.deR","group":2},{"name":"Isabeau","group":2},{"name":"Gervais","group":2},{"name":"Tholomyes","group":3},{"name":"Listolier","group":3},{"name":"Fameuil","group":3},{"name":"Blacheville","group":3},{"name":"Favourite","group":3},{"name":"Dahlia","group":3},{"name":"Zephine","group":3},{"name":"Fantine","group":3},{"name":"Mme.Thenardier","group":4},{"name":"Thenardier","group":4},{"name":"Cosette","group":5},{"name":"Javert","group":4},{"name":"Fauchelevent","group":0},{"name":"Bamatabois","group":2},{"name":"Perpetue","group":3},{"name":"Simplice","group":2},{"name":"Scaufflaire","group":2},{"name":"Woman1","group":2},{"name":"Judge","group":2},{"name":"Champmathieu","group":2},{"name":"Brevet","group":2},{"name":"Chenildieu","group":2},{"name":"Cochepaille","group":2},{"name":"Pontmercy","group":4},{"name":"Boulatruelle","group":6},{"name":"Eponine","group":4},{"name":"Anzelma","group":4},{"name":"Woman2","group":5},{"name":"MotherInnocent","group":0},{"name":"Gribier","group":0},{"name":"Jondrette","group":7},{"name":"Mme.Burgon","group":7},{"name":"Gavroche","group":8},{"name":"Gillenormand","group":5},{"name":"Magnon","group":5},{"name":"Mlle.Gillenormand","group":5},{"name":"Mme.Pontmercy","group":5},{"name":"Mlle.Vaubois","group":5},{"name":"Lt.Gillenormand","group":5},{"name":"Marius","group":8},{"name":"BaronessT","group":5},{"name":"Mabeuf","group":8},{"name":"Enjolras","group":8},{"name":"Combeferre","group":8},{"name":"Prouvaire","group":8},{"name":"Feuilly","group":8},{"name":"Courfeyrac","group":8},{"name":"Bahorel","group":8},{"name":"Bossuet","group":8},{"name":"Joly","group":8},{"name":"Grantaire","group":8},{"name":"MotherPlutarch","group":9},{"name":"Gueulemer","group":4},{"name":"Babet","group":4},{"name":"Claquesous","group":4},{"name":"Montparnasse","group":4},{"name":"Toussaint","group":5},{"name":"Child1","group":10},{"name":"Child2","group":10},{"name":"Brujon","group":4},{"name":"Mme.Hucheloup","group":8}],"links":[{"source":1,"target":0,"value":1},{"source":2,"target":0,"value":8},{"source":3,"target":0,"value":10},{"source":3,"target":2,"value":6},{"source":4,"target":0,"value":1},{"source":5,"target":0,"value":1},{"source":6,"target":0,"value":1},{"source":7,"target":0,"value":1},{"source":8,"target":0,"value":2},{"source":9,"target":0,"value":1},{"source":11,"target":10,"value":1},{"source":11,"target":3,"value":3},{"source":11,"target":2,"value":3},{"source":11,"target":0,"value":5},{"source":12,"target":11,"value":1},{"source":13,"target":11,"value":1},{"source":14,"target":11,"value":1},{"source":15,"target":11,"value":1},{"source":17,"target":16,"value":4},{"source":18,"target":16,"value":4},{"source":18,"target":17,"value":4},{"source":19,"target":16,"value":4},{"source":19,"target":17,"value":4},{"source":19,"target":18,"value":4},{"source":20,"target":16,"value":3},{"source":20,"target":17,"value":3},{"source":20,"target":18,"value":3},{"source":20,"target":19,"value":4},{"source":21,"target":16,"value":3},{"source":21,"target":17,"value":3},{"source":21,"target":18,"value":3},{"source":21,"target":19,"value":3},{"source":21,"target":20,"value":5},{"source":22,"target":16,"value":3},{"source":22,"target":17,"value":3},{"source":22,"target":18,"value":3},{"source":22,"target":19,"value":3},{"source":22,"target":20,"value":4},{"source":22,"target":21,"value":4},{"source":23,"target":16,"value":3},{"source":23,"target":17,"value":3},{"source":23,"target":18,"value":3},{"source":23,"target":19,"value":3},{"source":23,"target":20,"value":4},{"source":23,"target":21,"value":4},{"source":23,"target":22,"value":4},{"source":23,"target":12,"value":2},{"source":23,"target":11,"value":9},{"source":24,"target":23,"value":2},{"source":24,"target":11,"value":7},{"source":25,"target":24,"value":13},{"source":25,"target":23,"value":1},{"source":25,"target":11,"value":12},{"source":26,"target":24,"value":4},{"source":26,"target":11,"value":31},{"source":26,"target":16,"value":1},{"source":26,"target":25,"value":1},{"source":27,"target":11,"value":17},{"source":27,"target":23,"value":5},{"source":27,"target":25,"value":5},{"source":27,"target":24,"value":1},{"source":27,"target":26,"value":1},{"source":28,"target":11,"value":8},{"source":28,"target":27,"value":1},{"source":29,"target":23,"value":1},{"source":29,"target":27,"value":1},{"source":29,"target":11,"value":2},{"source":30,"target":23,"value":1},{"source":31,"target":30,"value":2},{"source":31,"target":11,"value":3},{"source":31,"target":23,"value":2},{"source":31,"target":27,"value":1},{"source":32,"target":11,"value":1},{"source":33,"target":11,"value":2},{"source":33,"target":27,"value":1},{"source":34,"target":11,"value":3},{"source":34,"target":29,"value":2},{"source":35,"target":11,"value":3},{"source":35,"target":34,"value":3},{"source":35,"target":29,"value":2},{"source":36,"target":34,"value":2},{"source":36,"target":35,"value":2},{"source":36,"target":11,"value":2},{"source":36,"target":29,"value":1},{"source":37,"target":34,"value":2},{"source":37,"target":35,"value":2},{"source":37,"target":36,"value":2},{"source":37,"target":11,"value":2},{"source":37,"target":29,"value":1},{"source":38,"target":34,"value":2},{"source":38,"target":35,"value":2},{"source":38,"target":36,"value":2},{"source":38,"target":37,"value":2},{"source":38,"target":11,"value":2},{"source":38,"target":29,"value":1},{"source":39,"target":25,"value":1},{"source":40,"target":25,"value":1},{"source":41,"target":24,"value":2},{"source":41,"target":25,"value":3},{"source":42,"target":41,"value":2},{"source":42,"target":25,"value":2},{"source":42,"target":24,"value":1},{"source":43,"target":11,"value":3},{"source":43,"target":26,"value":1},{"source":43,"target":27,"value":1},{"source":44,"target":28,"value":3},{"source":44,"target":11,"value":1},{"source":45,"target":28,"value":2},{"source":47,"target":46,"value":1},{"source":48,"target":47,"value":2},{"source":48,"target":25,"value":1},{"source":48,"target":27,"value":1},{"source":48,"target":11,"value":1},{"source":49,"target":26,"value":3},{"source":49,"target":11,"value":2},{"source":50,"target":49,"value":1},{"source":50,"target":24,"value":1},{"source":51,"target":49,"value":9},{"source":51,"target":26,"value":2},{"source":51,"target":11,"value":2},{"source":52,"target":51,"value":1},{"source":52,"target":39,"value":1},{"source":53,"target":51,"value":1},{"source":54,"target":51,"value":2},{"source":54,"target":49,"value":1},{"source":54,"target":26,"value":1},{"source":55,"target":51,"value":6},{"source":55,"target":49,"value":12},{"source":55,"target":39,"value":1},{"source":55,"target":54,"value":1},{"source":55,"target":26,"value":21},{"source":55,"target":11,"value":19},{"source":55,"target":16,"value":1},{"source":55,"target":25,"value":2},{"source":55,"target":41,"value":5},{"source":55,"target":48,"value":4},{"source":56,"target":49,"value":1},{"source":56,"target":55,"value":1},{"source":57,"target":55,"value":1},{"source":57,"target":41,"value":1},{"source":57,"target":48,"value":1},{"source":58,"target":55,"value":7},{"source":58,"target":48,"value":7},{"source":58,"target":27,"value":6},{"source":58,"target":57,"value":1},{"source":58,"target":11,"value":4},{"source":59,"target":58,"value":15},{"source":59,"target":55,"value":5},{"source":59,"target":48,"value":6},{"source":59,"target":57,"value":2},{"source":60,"target":48,"value":1},{"source":60,"target":58,"value":4},{"source":60,"target":59,"value":2},{"source":61,"target":48,"value":2},{"source":61,"target":58,"value":6},{"source":61,"target":60,"value":2},{"source":61,"target":59,"value":5},{"source":61,"target":57,"value":1},{"source":61,"target":55,"value":1},{"source":62,"target":55,"value":9},{"source":62,"target":58,"value":17},{"source":62,"target":59,"value":13},{"source":62,"target":48,"value":7},{"source":62,"target":57,"value":2},{"source":62,"target":41,"value":1},{"source":62,"target":61,"value":6},{"source":62,"target":60,"value":3},{"source":63,"target":59,"value":5},{"source":63,"target":48,"value":5},{"source":63,"target":62,"value":6},{"source":63,"target":57,"value":2},{"source":63,"target":58,"value":4},{"source":63,"target":61,"value":3},{"source":63,"target":60,"value":2},{"source":63,"target":55,"value":1},{"source":64,"target":55,"value":5},{"source":64,"target":62,"value":12},{"source":64,"target":48,"value":5},{"source":64,"target":63,"value":4},{"source":64,"target":58,"value":10},{"source":64,"target":61,"value":6},{"source":64,"target":60,"value":2},{"source":64,"target":59,"value":9},{"source":64,"target":57,"value":1},{"source":64,"target":11,"value":1},{"source":65,"target":63,"value":5},{"source":65,"target":64,"value":7},{"source":65,"target":48,"value":3},{"source":65,"target":62,"value":5},{"source":65,"target":58,"value":5},{"source":65,"target":61,"value":5},{"source":65,"target":60,"value":2},{"source":65,"target":59,"value":5},{"source":65,"target":57,"value":1},{"source":65,"target":55,"value":2},{"source":66,"target":64,"value":3},{"source":66,"target":58,"value":3},{"source":66,"target":59,"value":1},{"source":66,"target":62,"value":2},{"source":66,"target":65,"value":2},{"source":66,"target":48,"value":1},{"source":66,"target":63,"value":1},{"source":66,"target":61,"value":1},{"source":66,"target":60,"value":1},{"source":67,"target":57,"value":3},{"source":68,"target":25,"value":5},{"source":68,"target":11,"value":1},{"source":68,"target":24,"value":1},{"source":68,"target":27,"value":1},{"source":68,"target":48,"value":1},{"source":68,"target":41,"value":1},{"source":69,"target":25,"value":6},{"source":69,"target":68,"value":6},{"source":69,"target":11,"value":1},{"source":69,"target":24,"value":1},{"source":69,"target":27,"value":2},{"source":69,"target":48,"value":1},{"source":69,"target":41,"value":1},{"source":70,"target":25,"value":4},{"source":70,"target":69,"value":4},{"source":70,"target":68,"value":4},{"source":70,"target":11,"value":1},{"source":70,"target":24,"value":1},{"source":70,"target":27,"value":1},{"source":70,"target":41,"value":1},{"source":70,"target":58,"value":1},{"source":71,"target":27,"value":1},{"source":71,"target":69,"value":2},{"source":71,"target":68,"value":2},{"source":71,"target":70,"value":2},{"source":71,"target":11,"value":1},{"source":71,"target":48,"value":1},{"source":71,"target":41,"value":1},{"source":71,"target":25,"value":1},{"source":72,"target":26,"value":2},{"source":72,"target":27,"value":1},{"source":72,"target":11,"value":1},{"source":73,"target":48,"value":2},{"source":74,"target":48,"value":2},{"source":74,"target":73,"value":3},{"source":75,"target":69,"value":3},{"source":75,"target":68,"value":3},{"source":75,"target":25,"value":3},{"source":75,"target":48,"value":1},{"source":75,"target":41,"value":1},{"source":75,"target":70,"value":1},{"source":75,"target":71,"value":1},{"source":76,"target":64,"value":1},{"source":76,"target":65,"value":1},{"source":76,"target":66,"value":1},{"source":76,"target":63,"value":1},{"source":76,"target":62,"value":1},{"source":76,"target":48,"value":1},{"source":76,"target":58,"value":1}]}
    data = simplejson.dumps(graph)
    if pk: template = 'data/vivagraph/graph' + pk + '.html'
    return render(request, template, {'data': data})


class VivaGraph(TemplateView):
    template_name = 'data/vivagraph.html'
    def dispatch(self, request, *args, **kwargs):
        if 'slug' in kwargs and kwargs['slug']:
            self.template_name = 'data/vivagraph/' + kwargs['slug'] + '.html'
        if 'pk' in kwargs:
            self.template_name = 'data/vivagraph/' + kwargs['pk'] + '.html'

        return super(VivaGraph, self).dispatch(request, *args, **kwargs)


def index(request):
    ctx = {'entry': get('Data App'),
           'hierarchy': get('Data Hierarchy'),
           'categories': get('Data Categories'),
           'tags': get('Data Tags')}
    return render_to_response('data/index.html', ctx,
        context_instance=RequestContext(request))

def hierarchy(request, template='data/hierarchy.html'):
    ctx = {'entry': get('Data Hierarchy'),
           'entries': Entry.objects.filter(published=True)}
    return render(request, template, ctx)

def entries(request): pass
def entry(): pass
def add_entry(): pass
def edit_entry(): pass
def remove_entry(): pass

def breadcrump(request, slug):
    #print("Breadcrump: %s" % slug)
    entry = Entry.objects.get(slug=slug)
    return render_to_response('entry_view.html', {'entry': entry},
        context_instance=RequestContext(request))

def changes(request, pk=None, template_name='data/change_list.html'):
    if pk:
        #print("pk = %s" % pk)
        query = Entry.objects.get(pk=int(pk))
        queryset = Change.objects.filter(of=query).order_by('-at')
        #queryset = query.updates.all()#.order_by('-created')
    else:
        queryset = Change.objects.filter(of__published=True).order_by('-at')
    ctx = {'object_list': queryset, 'object': query}
    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))

def change(request, slug, template='data/change.html'):
    change = Change.objects.get(slug=slug)
    changes = change.differences()
    ctx = {'change': change, 'changes': changes}
    return render(template, ctx)

def remove_change(request, slug):
    #print("remove_change: slug = %s" % slug)
    change = Change.objects.get(slug=slug)
    change.delete()
    msg = 'Successfully removed change %s' % change.title
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/data/changes/%s' % change.of.pk)


class ChangeView(DetailView):
    pk = None
    slug = None
    template_name = 'data/change.html'
    object_name = 'change'

    def dispatch(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            self.slug = kwargs['slug']
        elif 'pk' in kwargs:
            self.pk = kwargs['pk']
        return super(ChangeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChangeView, self).get_context_data(**kwargs)
        context['changes'] = self.object.differences()
        return context

    def get_queryset(self):
        if self.slug:
            objects = Change.objects.filter(slug=self.slug)
        else:
            objects = Change.objects.filter(pk=self.pk)
        return objects


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


class EntryList(ListView, FormView):
    queryset = Entry.objects.filter(published=True).order_by('-created')
    form_class = FilterForm
    query = None
    success_url = "/data/entries/list/"

    def form_valid(self, form):
        EntryList.query = form.cleaned_data['filter']
        return super(EntryList, self).form_valid(form)

    def form_invalid(self, form):
        EntryList.query = None
        return super(EntryList, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntryList, self).get_context_data(**kwargs)
        context['form'] = FilterForm(initial={'filter': EntryList.query})
        context['filterset'] = self.filterset
        context['entry'] = get('Data Entries')
        context['count'] = self.count
        return context

    def get_queryset(self):
        qs = self.queryset
        if EntryList.query:
            terms = EntryList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(title__icontains=term) |
                               Q(text__icontains=term))
        self.filterset = EntryFilterSet(qs, self.request.GET)
        self.count = self.filterset.qs.count()
        return self.filterset.qs


class ChangeList(ListView):
    queryset = Change.objects.filter(of__published=True).order_by('-at')
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ChangeList, self).get_context_data(**kwargs)
        context['entry'] = get('Changes')
        return context


class TagDetail(ListView):
    #def fill_context(self):
        #self.request

    def dispatch(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            tag = Tag.objects.get(slug=kwargs['slug'])
        else:
            tag = Tag.objects.get(pk=kwargs['pk'])
        items = TaggedItem.objects.filter(tag__pk=tag.pk)
        #for item in items:
        #    print("Item: %s;" % vars(item))
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


class Generate(Create):
    """Enables th creation of data entry with initial values."""
    comment = 'Generated entry.'
    message = 'Successfully generated %s'
    action = 'Generate'
    def dispatch(self, request, *args, **kwargs):
        if 'title' in kwargs:
            self.title = kwargs['title']
            del kwargs['title']
        return super(Generate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(Generate, self).get_initial()
        initial = initial.copy()
        initial['title'] = self.title
        del self.title
        return initial


class GenerateRelation(Create):
    model = Relation
    form_class = RelationForm
    comment = 'Generated relation.'
    message = 'Successfully generated %s'
    action = 'Generate'
    def dispatch(self, request, *args, **kwargs):
        self.source = kwargs['source']
        self.type = kwargs['type']
        self.target = kwargs['target']
        del kwargs['source']
        del kwargs['type']
        del kwargs['target']
        return super(GenerateRelation, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(GenerateRelation, self).get_initial()
        try: initial['fr'] = Entry.objects.get(title__icontains=self.source.replace('_', ' ')).pk
        except: pass
        try: initial['be'] = Entry.objects.get(title__icontains=self.type.replace('_', ' ')).pk
        except: pass
        try: initial['to'] = Entry.objects.get(title__icontains=self.target.replace('_', ' ')).pk
        except: pass
        del self.source
        del self.type
        del self.target

        return initial



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
    model = Entry
    def dispatch(self, request, *args, **kwargs):
        #print("data.views.EntryView.dispatch: args=%s, kwargs=%s" % (args, kwargs))
        if 'slug' in kwargs:
            self.slug = kwargs['slug']
        return super(EntryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        objects = self.model.objects.filter(slug=self.slug)
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


class CategoryList(ListView):
    queryset = Category.objects.all()
    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['entry'] = get('Data Categories')
        return context

class Entries(TableFilter):
    table_class = EntryTable
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(Entries, self).get_context_data(**kwargs)
        context['entry'] = get('Data Entries')
        return context


class RelationList(ListView):
    queryset = Relation.objects.all()
    def get_context_data(self, **kwargs):
        context = super(RelationList, self).get_context_data(**kwargs)
        context['entry'] = get('Relations')
        return context


class AlterationList(ListView):
    queryset = Alteration.objects.all().order_by('-at')
    def get_context_data(self, **kwargs):
        context = super(AlterationList, self).get_context_data(**kwargs)
        context['entry'] = get('Alterations')
        return context


class TagList(ListView):
    queryset = Tag.objects.all()
    template_name = "data/tag_list.html"
    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['entry'] = get('Data Tags')
        return context


class HierarchyList(EntryList):
    context_object_name = 'entries'
    template_name = 'data/hierarchy.html'
    def get_context_data(self, **kwargs):
        context = super(HierarchyList, self).get_context_data(**kwargs)
        context['entry'] = get('Data Hierarchy')
        return context


def newEntry(request):
    return handlePopAdd(request, EntryForm, 'entry')