"""Annotation views."""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView, UpdateView

import reversion

from models import Classification, Tissue, Species, Taxonomy
from forms import (ClassificationForm, DeleteClassificationForm,
                   TissueForm, DeleteTissueForm,
                   SpeciesForm)

from meta.view import log
from data import get


def index(request):
    annotations = get("Annotations")
    return render_to_response('annotations/index.html',
                              {'annotations': annotations},
                               context_instance=RequestContext(request))

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

def add_classification(request):
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
            return redirect('/annotations/classification/%s' % classification.pk)
    return render_to_response('annotations/classification_form.html', {'form': form},
        context_instance=RequestContext(request))

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
                msg = "Successfully deleted classification %s." % classification.title
                messages.add_message(request, messages.SUCCESS, _(msg))
                return redirect('/annotations/classifications/')
    ctx = {'classification': classification, 'form': form}
    return render_to_response('annotations/delete_classification.html', ctx,
        context_instance=RequestContext(request))

def species(request):
    species = Species.objects.filter(main_model=True).order_by('complexity')
    return render_to_response('annotations/species.html', {'species': species},
                              context_instance=RequestContext(request))         

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
    print attributes
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



def tissues(request):
    """Lists all the tissues with pagination (Pagination is not yet implemented)."""
    tissues = Tissue.objects.all()
    return render_to_response('annotations/tissues.html', {'tissues': tissues},
                              context_instance=RequestContext(request))

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

def tissue_archive(request):
    """Generates a simple archive list of all the tissues
    (with and without pagination on click)."""
    tissues = Tissue.objects.all()
    ctx = {'tissues': tissues}
    return render_to_response('annotations/tissue_archive.html', ctx,
                              context_instance=RequestContext(request))

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
            print tissue, form.is_valid()
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


class TissueCreate(TissueView, CreateView):
    pass


class TissueUpdate(TissueView, CreateView):
    pass


#234567891123456789212345678931234567894123456789512345678961234567897123456789
