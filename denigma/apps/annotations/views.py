"""Annotation views."""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.db import connection
from django.contrib.auth.decorators import permission_required

from django_tables2 import RequestConfig

import reversion

from data.filters import TableFilter
from meta.view import log
from data import get
from add.forms import handlePopAdd

from models import Classification, Tissue, Species, Taxonomy
from forms import (ClassificationForm, DeleteClassificationForm,
                   TissueForm, DeleteTissueForm,
                   SpeciesForm, AnimalForm)
from tables import TissueTable
from filters import  TissueFilterSet


def index(request, template='annotations/index.html'):
    annotations = get("Annotations")
    return render(request, template, {'annotations': annotations})

def bulk_upload(request):
    """Bulk upload function for annotation data."""
    model_name = request.POST['model']
    data = request.POST['data'].split('\n')
    for line in data:
        if line == data[0]:
            header = {}
            headers = line.split('\t')
            model = eval(model_name+'()')
            for index, head in enumerate(headers):
                if hasattr(model, head):
                    header[index] = head
            continue
        elif not line: continue
        columns = line.split('\t')
        model = eval(model_name+'()')
        for index, column in enumerate(columns):
            if index in header:
                setattr(model, header[index], column)
        model.save()
    msg = "Received %s lines of data on %s for model %s"\
          % (len(data)-1, header.values(), model_name)
    messages.add_message(request, messages.SUCCESS, ugettext(msg))
    return HttpResponseRedirect('/annotations/')

#def bulk_upload(request):
#   return render_to_response('annotations/bulk_upload.html',
#                             context_instance=RequestContext(request))




def classifications(request):
    entry = get("Classifications")
    classifications = Classification.objects.all()
    return render_to_response('annotations/classifications.html',
                              {'nodes': classifications, 'entry': entry},
                              context_instance=RequestContext(request))

def classification(request, pk):
    classification = Classification.objects.get(pk=pk)
    return render_to_response('annotations/classification.html',
                              {'classification': classification},
                              context_instance=RequestContext(request))

@login_required
def edit_classification(request, pk):
    classification = Classification.objects.get(pk=pk)
    form = ClassificationForm(request.POST or None, instance=classification)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/annotations/classifications/')
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed classification"
            reversion.set_comment(comment)
            log(request, classification, comment)
        return redirect('/annotations/classification/%s' % pk)
    ctx = {'classification': classification,
           'form': form,
           'action': 'Edit'}
    return render_to_response('annotations/classification_form.html', ctx,
        context_instance=RequestContext(request))

def add_classification(request, template='annotations/classification_form.html'):
    form = ClassificationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with reversion.create_revision():
            classification = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Added classification"
            reversion.set_comment(comment)
            log(request, classification, comment)
            msg = "Successfully added classification."
            messages.add_message(request, messages.SUCCESS, _(msg))
            return redirect('/annotations/classification/%s' %
                            classification.pk)
    return render(request, template, {'form': form, 'action': 'Add'})


@login_required
def delete_classification(request, pk):
    classification = Classification.objects.get(pk=pk)
    form = DeleteClassificationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/annotations/classification/%s' % pk)
        elif "delete_classification" in request.POST:
            with reversion.create_revision():
                classification.delete()
                reversion.set_user(request.user)
                comment = request.POST['comment'] or "Delete classification"
                log(request, classification, comment)
                msg = "Successfully deleted classification %s." % \
                      classification.title
                messages.add_message(request, messages.SUCCESS, _(msg))
                return redirect('/annotations/classifications/')
    ctx = {'classification': classification, 'form': form}
    return render_to_response('annotations/delete_classification.html', ctx,
        context_instance=RequestContext(request))

def species(request, template='annotations/species.html'):
    entry = get("Species")
    species = Species.objects.filter(main_model=True).order_by('complexity')
    others = Species.objects.filter(main_model=False)
    return render(request, template, {'entry': entry, 'species': species, 'others': others})

def species_details(request, pk):
    species = Species.objects.get(pk=pk)
    ctx = {'species': species}
    return render_to_response('annotations/species_details.html', ctx,
                              context_instance=RequestContext(request))

def species_archive(request):
    species = Taxonomy.objects.all()
    paginator = Paginator(species, 25)
    page_num = request.GET.get('page', 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)
    ctx = {'page': page}
    return render_to_response('annotations/species_archive.html', ctx,
                              context_instance=RequestContext(request))

def species_detailed(request, pk):
    species = Taxonomy.objects.get(pk=pk)
    attributes = dict([(attr, value) for (attr, value) in vars(species).items()\
                      if value and not attr.startswith('_')])
    #print attributes
    ctx = {'species': species, 'attributes': attributes}
    return render_to_response('annotations/species_detailed.html', ctx,
                              context_instance=RequestContext(request))

@login_required
def edit_species(request, pk):
    species = Species.objects.get(pk=pk)
    form = SpeciesForm(request.POST or None, instance=species)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/annotations/species/%s' % pk)
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed tissue"
            reversion.set_comment(comment)
            log(request, species, comment)
            return redirect('/annotations/species/%s.html' % pk)
    ctx = {'species': species, 'form': form, 'action': 'Edit'}
    return render_to_response('annotations/species_form.html', ctx,
        context_instance=RequestContext(request))


class SpeciesView(object):
    form_class = SpeciesForm
    model = Species


class SpeciesUpdate(SpeciesView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(SpeciesView, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class SpeciesCreate(SpeciesView, CreateView):
    def get_context_data(self, **kwargs):
        context = super(SpeciesView, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        return context


def tissues(request, template='annotations/tissues.html'):
    """Lists all the tissues with pagination (Pagination is not yet implemented)."""
    tissues = Tissue.objects.all()
    return render(request, template, {'tissues': tissues})


def tissue(request, pk=None, name=None):
    """Gives a the details of a specific tissue/cell type."""
    if pk:
        tissue = Tissue.objects.get(pk=pk)
    elif name:
        try:
            tissue = Tissue.objects.get(name=name)
        except: # Better implement slug, rather than name.
            tissue = Tissue.objects.get(name=name.replace('-', ' '))
    return render_to_response('annotations/tissue.html', {'tissue': tissue},
                              context_instance=RequestContext(request))

def tissue_archive(request, template='annotations/tissue_archive.html'):
    """Generates a simple archive list of all the tissues
    (with and without pagination on click)."""
    tissues = Tissue.objects.all()
    ctx = {'tissues': tissues}
    return render(request, template, ctx)

def add_tissue(request):
    form = TissueForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with reversion.create_revision():
            tissue = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = "Added tissue. %s" % request.POST['comment'] or ''
            reversion.set_comment(comment)
            log(request, tissue, comment)
            msg = "Successfully added tissue."
            messages.add_message(request, messages.SUCCESS, ugettext(msg))
            return redirect('/annotations/tissue/%s' % tissue.pk)
    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('annotations/tissue_form.html', ctx,
        context_instance=RequestContext(request))

@login_required
def edit_tissue(request, pk):
    tissue = Tissue.objects.get(pk=pk)
    form = TissueForm(request.POST or None, instance=tissue)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/annotations/tissue/%s' % pk)
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed tissue."
            reversion.set_comment(comment)
            log(request, tissue, comment)
            return redirect('/annotations/tissue/%s' % pk)
    ctx = {'tissue': tissue, 'form': form, 'action': 'Edit'}
    return render_to_response('annotations/tissue_form.html', ctx,
        context_instance=RequestContext(request))

@login_required
def delete_tissue(request, pk):
    tissue = Tissue.objects.get(pk=pk)
    form = DeleteTissueForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        if "cancel" in request.POST:
            return redirect('/annotations/tissue/%s' % pk)
        elif "delete" in request.POST:
            #print tissue, form.is_valid()
            with reversion.create_revision():
                tissue.delete()
                reversion.set_user(request.user)
                comment = request.POST['comment'] or "Changed tissue"
                reversion.set_comment(comment)
                log(request, tissue, comment)
                return redirect('/annotations/tissues/')
    ctx = {'tissue': tissue, 'form': form}
    return render_to_response('annotations/delete_tissue.html', ctx,
        context_instance=RequestContext(request))


class TissueView(object):
    form_class = TissueForm
    model = Tissue


def tissue_table(request, template='annotations/tissue_list.html'):
    table = TissueTable(Tissue.objects.all())
    RequestConfig(request).configure(table)
    return render(request, template, {'table': table})


class TissueList(TableFilter):
    model = Tissue
    table_class = TissueTable
    template_name = 'annotations/tissues.html'
    queryset = Tissue.objects.all()
    filterset = TissueFilterSet
    success_url = '/annotations/tissues/'

    def get_context_data(self, **kwargs):
        context = super(TissueList, self).get_context_data(**kwargs)
        context['entry'] = get('Tissues')
        return context

    def get_queryset(self):
        qs = Tissue.objects.all()
        if TissueList.query:
            terms = TissueList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(name__icontains=TissueList.query) |
                               Q(description__icontains=TissueList.query) |
                               Q(synonyms__icontains=TissueList.query) |
                               Q(notes__icontains=TissueList.query))
        self.filterset = TissueFilterSet(qs, self.request.GET)
        return self.filterset.qs.order_by('identifier')


class TissueCreate(TissueView, CreateView):
    pass


class TissueUpdate(TissueView, CreateView):
    pass


def tissue_hierarchy(request):
    """Builds up the hierarchy of tissues."""
    Tissue.objects.rebuild()
    tissues = Tissue.objects.all().order_by('identifier')
    previous = None
    for tissue in tissues:
        #print("%s %s %s" % (tissue.identifier,tissue.hierarchy, tissue))
        if tissue.hierarchy == None: continue
        elif not previous:
            #print("Setting tissue %s as previous" % tissue)
            previous = {0:tissue}
        else:
            if tissue.hierarchy != 0:
                tissue.parent = previous[tissue.hierarchy-1]
                #print("parent is %s" % previous[tissue.hierarchy-1])
                tissue.save()
            else:
                Tissue.objects.rebuild()
            previous[tissue.hierarchy] = tissue
            previous_level = tissue.hierarchy
    msg = _("Successfully build hierarchy.")
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('/annotations/tissues/')


def newAnimal(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, AnimalForm, 'alternative_names')

def newClassification(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, ClassificationForm, 'classifications')

#234567891123456789212345678931234567894123456789512345678961234567897123456789