# -*- coding: utf-8 -*-
import csv
import json

from Bio import Entrez
Entrez.email = "age@liv.ac.uk"

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response,redirect, render
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
#from django.core.urlresolvers import reverse # reverse_lazy (Django 1.4)
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.views.generic.edit import CreateView, UpdateView, FormView # DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q


import reversion

from django_tables2 import SingleTableView, RequestConfig

from blog.models import Post

from add.forms import handlePopAdd

from meta.view import log

from home.views import LoginRequiredMixin

import data
from data import get
from data.views import Create, Update, Delete

from datasets.models import Reference

from annotations.models import Species, GO
from annotations.models import Classification, Ortholog, HomoloGene, InParanoid, gene2ensembl

from expressions.views import functional_enrichment

from utils.dumper import dump

from models import (Study, Experiment, Measurement, Comparison, Intervention, Factor, Regimen, Strain, Assay,
                   Manipulation, Variant, State, Population, Technology, StudyType, ORType, VariantType)

from forms import (StudyForm, EditStudyForm, DeleteStudyForm,
                   ExperimentForm, DeleteExperimentForm,
                   ComparisonForm, VariantTypeForm, ORTypeForm,
                   InterventionForm, DeleteInterventionForm, InterventionFilterSet,
                   FactorForm, StrainForm, StateForm, TechnologyForm, StudyTypeForm, PopulationForm,
                   FilterForm, FactorFilterSet, VariantForm, VariantFilterSet, VariantBulkInsertForm, OntologyForm)
from tables import ComparisonTable, InterventionTable, FactorTable, VariantTable


def index(request):
    lifespan = get(title="Lifespan")
    return render_to_response('lifespan/index.html', {'lifespan': lifespan},
                              context_instance=RequestContext(request))

def studies(request):
    studies = Study.objects.all().order_by('-created')
    species = Species.objects.all().order_by('complexity')

    count = studies.count()
    integrated = studies.filter(integrated=True).count()

    paginator = Paginator(studies, 5)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    ctx = {'page': page,
           'count': count,
           'integrated': integrated, 'request':request,
           'species': species}
    return render_to_response('lifespan/studies.html', ctx,
                              context_instance=RequestContext(request))

def study(request, pk):
    study = Study.objects.get(pk=pk)
    experiments = study.experiment_set.all()
    interventions = Intervention.objects.filter(references=study.reference)
    ctx = {'study': study,
           'experiments': experiments,
           'interventions': interventions
    }
    return render_to_response('lifespan/study.html', ctx,
                              context_instance=RequestContext(request))
#@reversion.create_revision()
def add_studies(request):
    titles = request.POST['titles'].replace('\r', '').split('\n')
    pmids = request.POST['pmids'].replace('\r', '').split('\n')
    taxid = request.POST.get('species', None)
    if taxid:
        species = Species.objects.get(taxid=taxid)

    comment = request.POST['comment'] or "Adding studies"

    succieded = []
    warned = []
    failed = []

    with reversion.create_revision():
        #print "Titles", titles
        #print "pmids", pmids
        for title in titles:
            if not title: continue
            #print "Title:", title
            #study, created = Study.objects.get_or_create(title=title)
            study = Study(title=title)
            study.save()
            try:
                print vars(study)
            except UnicodeEncodeError as e:
                print e
            print study.reference_was_created
            if not study.reference_was_created:#study.reference.authors:
                warned.append(title)
                messages.add_message(request, messages.WARNING, ugettext("Already in db: %s" % title))
                created = False
            else:
                created = True
            try:
                study_confirm = Study.objects.get(title__icontains=title)
                if study_confirm:
                    succieded.append(title)
                    print "Authors:", study.reference.authors
                    messages.add_message(request, messages.SUCCESS, ugettext("Succeeded: %s" % title))
                else:
                    failed.append(title)
                    messages.add_message(request, messages.ERROR, ugettext("Failed: %s" % title))

                if taxid:
                    study_confirm.species.add(species)
                    print("Adding species")
                    #study_confirm.save()

            except Exception as e:
                print e
                failed.append(title)
                messages.add_message(request, messages.ERROR, ugettext("Failed: %s" % title))
                messages.add_message(request, messages.WARNING, ugettext("However added %s" % study.title))
                if taxid:
                    print("Adding species")
                    try:
                        study.species.add(species)
                    except ValueError as e: #Exception Value: 'Study' instance needs to have a primary key value before a many-to-many relationship can be used.
                        messages.add_message(request, messages.ERROR, ugettext("Error: %s" % e))
            log(request, study, comment)


        for pmid in pmids:
            if not pmid: continue
            print "PMID:", pmid
            study = Study(pmid=pmid)
            study.save()
            #print "views.add.studies for pmid in pmids:", vars(study)
            if not study.reference_was_created:
                warned.append(pmid)
                messages.add_message(request, messages.WARNING, ugettext("Already in db: %s" % pmid))
                created = False
            else:
                created = True
            try:
                study_confirm = Study.objects.get(pmid=pmid)
                if study_confirm:
                    succieded.append(pmid)
                    messages.add_message(request, messages.SUCCESS, ugettext("Succeeded: %s" % pmid))
                else:
                    failed.append(pmid)
                    messages.add_message(request, messages.ERROR, ugettext("Failed: %s" % pmid))

                if taxid:
                    print("Adding species")
                    study_confirm.species.add(species)

            except Exception as e:
                print e
                failed.append(pmid)
                messages.add_message(request, messages.ERROR, ugettext("Failed: %s" % pmid))
                messages.add_message(request, messages.WARNING, ugettext("However added %s" % study.pmid))
                if taxid:
                    print("Adding species")
                    try:
                        study.species.add(species)
                    except ValueError as e:
                        messages.add_message(request, messages.ERROR, ugettext("Error: %s" % e))

            log(request, study, comment)
        if isinstance(request.user, AnonymousUser):
            request.user = User.objects.get(username="Anonymous")
        reversion.set_user(request.user)
        reversion.set_comment(comment)

    if succieded:
        msg = "Successfully added the following %i studies: \n%s" % (len(succieded), "\n".join(succieded))
        messages.add_message(request, messages.SUCCESS, ugettext(msg))
    if warned:
        msg = "Found already in db the following %i studies: \n%s" % (len(warned), "\n".join(warned))
        messages.add_message(request, messages.WARNING, ugettext(msg))
    if failed:
        msg = "Failed to fetch information on the following %i studies: \n%s" % (len(failed), "\n".join(failed))
        messages.add_message(request, messages.ERROR, ugettext(msg))

    return HttpResponseRedirect('/lifespan/studies/')

@login_required
def edit_study(request, pk):
    study = Study.objects.get(pk=pk)
    if request.method == "GET":
        form = EditStudyForm(instance=study)
    elif request.method == "POST":
        if "cancel" in request.POST:
            return redirect('/lifespan/studies/')
        with reversion.create_revision():
            form = EditStudyForm(request.POST, instance=study)

            if form.is_valid():
                form.save()
                reversion.set_user(request.user)
                comment = request.POST['comment'] or "Changed study"
                reversion.set_comment(comment)
                log(request, study, comment)
                return redirect('/lifespan/study/%s' % pk)
    else:
        form = EditStudyForm(instance=study)
    ctx = {'form': form, 'study': study}
    return render_to_response('lifespan/edit_study.html', ctx,
        context_instance=RequestContext(request))

@login_required
def delete_study(request, pk):
    """Depricated."""
    with reversion.create_revision():
        study = Study.objects.get(pk=pk)
        study.delete()
        reversion.set_user(request.user)
        reversion.set_comment(request.POST['comment'] or "Deleted study")
    return redirect('/lifespan/studies/')

@login_required
def delete_study(request, pk):
    try:
        study = Study.objects.get(pk=pk)
    except ObjectDoesNotExist:
        msg = "Error study matching query does not exist."
        messages.add_message(request, messages.ERROR, ugettext(msg))
        return redirect('/lifespan/studies/')
    form = DeleteStudyForm(request.POST or None)
    if request.method == "POST" and form.is_valid:
        if 'cancel' in request.POST:
            return redirect('/lifespan/study/%s' % pk)
        else:
            with reversion.create_revision():
                try:
                    if 'delete_study' in request.POST:
                        study.delete()
                    if 'delete_reference' in request.POST:
                        study.delete()
                        study.reference.delete()
                except AttributeError:
                    msg = "Error study did not have a reference associated."
                    messages.add_message(request, messages.ERROR, ugettext(msg))
                reversion.set_user(request.user)
                comment = request.POST['comment'] or "Deleted study"
                reversion.set_comment(comment)
                log(request, study, comment)
                return redirect('/lifespan/studies/')
    ctx = {'study': study, 'form': form}
    return render_to_response('lifespan/delete_study.html', ctx,
                context_instance=RequestContext(request))

def studies_archive(request):
    studies = Study.objects.all().order_by('-created')
    return render_to_response('lifespan/studies_archive.html', {'studies': studies},
                              context_instance=RequestContext(request))

def experiments(request):
    experiments = Experiment.objects.all()
    try: experiments_entry = Entry.objects.get(title="Experiments")
    except: experiments_entry = {'text': "Lifespan experiments."}
    ctx = {'experiments': experiments, 'experiments_entry': experiments_entry}
    return render_to_response('lifespan/experiments.html',ctx,
                              context_instance=RequestContext(request))

def experiment(request, pk):
    experiment = Experiment.objects.get(pk=pk)
    comparisons = Comparison.objects.filter(exp__experiment=experiment)
    table = ComparisonTable(comparisons)
    RequestConfig(request).configure(table)
    ctx = {'experiment': experiment, 'comparisons': comparisons, 'table': table}
    return render_to_response('lifespan/experiment.html', ctx,
                              context_instance=RequestContext(request))

def add_experiment(request, pk):
    form = ExperimentForm(request.POST or None, pk=pk) # A form bound to the POST data
    if request.method == "POST" and form.is_valid(): # All validation rules pass
        with reversion.create_revision():
            experiment = form.save(commit=False)
            #print("Experiment id: %s" % experiment.id)
            #print form
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = "Added experiment."
            reversion.set_comment(comment)
            log(request, experiment, comment)
            msg = "Successfully added experiment."
            messages.add_message(request, messages.SUCCESS, ugettext(msg))
            return redirect('/lifespan/experiment/%s' % experiment.pk)
    return render_to_response('lifespan/add_experiment.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required
def edit_experiment(request, pk):
    experiment = Experiment.objects.get(pk=pk)
    form = ExperimentForm(request.POST or None, instance=experiment)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/lifespan/experiments/')
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed experiment"
            reversion.set_comment(comment)
            log(request, experiment, comment)
        return redirect('/lifespan/experiment/%s' % pk)
    ctx = {'experiment': experiment, 'form': form}
    return render_to_response('lifespan/edit_experiment.html', ctx,
        context_instance=RequestContext(request))

@login_required
def delete_experiment(request, pk):
    experiment = Experiment.objects.get(pk=pk)
    form = DeleteExperimentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if 'cancel' in request.POST:
            return redirect('/lifespan/experiment/%s' % pk)
        elif 'delete_experiment' in request.POST:
            with reversion.create_revision():
                experiment.delete()
                reversion.set_user(request.user)
                comment = request.POST['comment'] or "Deleted experiment"
                reversion.set_comment(comment)
                log(request, experiment, comment)
                return redirect('/lifespan/experiments/')
    ctx = {'experiment': experiment, 'form': form}
    return render_to_response('lifespan/delete_experiment.html', ctx,
        context_instance=RequestContext(request))

def measurements(request):
    measurements = Measurement.objects.all()
    return render_to_response('lifespan/measurements.html', {'measurements': measurements},
                            context_instance=RequestContext(request))


def comparisons(request):
    table = ComparisonTable(Comparison.objects.all())
    RequestConfig(request).configure(table)
    return render_to_response("lifespan/comparisons.html", {'comparisons': table},
        context_instance=RequestContext(request))

@login_required
def comparison(request, pk):
    comparison = Comparison.objects.get(pk=pk)
    form = ComparisonForm(request.POST or None, instance=comparison)
    #print("lifespan comparison")
    if request.POST and form.is_valid():
        #print("lifespan.views.comparison: form.is_valid()")
        form.save()
        msg = "Successfully changed comparison"
        messages.add_message(request, messages.SUCCESS, _(msg))
        redirect('/comparison/%s' % pk)
    ctx = {'comparison': comparison, 'form': form}
    return render_to_response('lifespan/comparison.html', ctx,
        context_instance=RequestContext(request))

def add_comparison(request, pk):
    return HttpResponse('Add comparison %s' % pk)

def edit_comparison(request, pk):
    return HttpResponse('Edit comparison %s' % pk)

"""Interventions"""
def interventions(request):
    interventions = Intervention.objects.all()
    ctx = {'interventions': interventions}
    return render_to_response("lifespan/interventions_archive.html", ctx,
        context_instance=RequestContext(request))

def intervention(request, pk):
    return HttpResponse("intervention")

def add_intervention(request):
    form = InterventionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with reversion.create_revision():
            intervention = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = "Added intervention. %s" % request.POST['comment'] or ''
            reversion.set_comment(comment)
            log(request, intervention, comment)
            msg = "Successfully added intervention."
            messages.add_message(request, messages.SUCCESS, ugettext(msg))
            return redirect('/lifespan/intervention/%s' % intervention.pk)
    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('lifespan/intervention_form.html', ctx,
        context_instance=RequestContext(request))

@login_required
def edit_intervention(request, pk):
    intervention = Intervention.objects.get(pk=pk)
    form = InterventionForm(request.POST or None, instance=intervention)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/lifespan/intervention/%s' % pk)
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed intervention"
            reversion.set_comment(comment)
            log(request, intervention, comment)
            return redirect('/lifespan/intervention/%s' % pk)
    ctx = {'intervention': intervention, 'form': form, 'action': 'Edit'}
    return render_to_response('lifespan/intervention_form.html', ctx,
        context_instance=RequestContext(request))

@login_required
def delete_intervention(request, pk):
    intervention = Intervention.objects.get(pk=pk)
    form = DeleteInterventionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if 'cancel' in request.POST:
            return redirect('/lifespan/intervention/%s' % pk)
        elif 'delete' in request.POST:
            with reversion.create_revision():
                intervention.delete()
                comment = request.POST['comment'] or "Delete intervention"
                reversion.set_comment(comment)
                log(request, intervention, comment)
                return redirect('/lifespan/interventions/')
    ctx = {'intervention': intervention, 'form': form}
    return render_to_response('lifespan/delete_intervention.html', ctx,
        context_instance=RequestContext(request))

@login_required
def remove_factor(request, pk):
    factor = Factor.objects.get(pk=pk)
    factor.delete()
    msg = 'Successfully removed %s' % factor
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/lifespan/')

#class DeleteFactor(Delete):
    #model = Factor


def link_interventions(request):
    interventions = Intervention.objects.all()
    for intervention in interventions:
        if intervention.taxid and not intervention.species:
            try: intervention.species = Species.objects.get(taxid=intervention.taxid)
            except Species.DoesNotExist as e:
                msg = "%s %s %s" % (intervention.name, intervention.taxid, e)
                messages.add_message(request, messages.ERROR, ugettext(msg))
        print intervention.taxid, intervention.species
    return redirect('/lifespan/')


class InterventionList(SingleTableView, FormView):
    queryset = Intervention.objects.all().order_by('-pk')
    template_name = 'lifespan/interventions.html' #_list
    context_object_name = 'interventions'
    table_class = InterventionTable
    model = Intervention
    form_class = FilterForm
    success_url = '/lifespan/interventions/'
    query = None

    def form_valid(self, form):
        InterventionList.query = form.cleaned_data['filter']
        return super(InterventionList, self).form_valid(form)

    def form_invalid(self, form):
        InterventionList.query = None
        return super(InterventionList, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(InterventionList, self).get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={'filter': InterventionList.query})
        context['interventionsfilter'] = self.interventionsfilter
        return context

    def get_queryset(self):
        if InterventionList.query:
            interventions = Intervention.objects.filter(Q(name__icontains=InterventionList.query) |
                                                        Q(effect__icontains=InterventionList.query)
                                                        ).order_by('-pk')
        else:
            interventions = Intervention.objects.all().order_by('-pk')
        self.interventionsfilter = InterventionFilterSet(interventions, self.request.GET)
        return self.interventionsfilter.qs


class InterventionView(object):
    form_class = InterventionForm
    model = Intervention

class InterventionCreate(InterventionView, CreateView):
    def get_context_data(self, **kwargs):
        context = super(InterventionCreate, self).get_context_data(**kwargs)
        context['action'] = 'Create'
        return context


class InterventionUpdate(InterventionView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(InterventionUpdate, self).get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

#
#class InterventionDelete(InterventionView, DeleteView):
#    success_url = reverse('lifespan/interventions') # reverse_lazy in Django 1.4

"""Factors"""
def factors(request, pk):
    factor = Factor.objects.get(pk=pk)
    return render_to_response('lifespan/factor.html', {'factor': factor},
        context_instance=RequestContext(request))

def factor(request, pk):
    return HttpResponse('factor')

@login_required
def add_factor(request):
    form = FactorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with reversion.create_revision():
            factor = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = "Added factor. %s" % request.POST['comment'] or ''
            reversion.set_comment(comment)
            log(request, factor, comment)
            msg = "Successfully added factor."
            messages.add_message(request, messages.SUCCESS, ugettext(msg))
            return redirect('/lifespan/factor/%s' % factor.pk)
    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('lifespan/factor_form.html', ctx,
        context_instance=RequestContext(request))

@login_required
def edit_factor(request, pk):
    factor = Factor.objects.get(pk=pk)
    form = FactorForm(request.POST or None, instance=factor)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/lifespan/factor/%s' % pk)
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed factor"
            reversion.set_comment(comment)
            log(request, factor, comment)
            return redirect('/lifespan/factor/%s' % pk)
    ctx = {'factor': factor, 'form': form, 'action': 'Edit'}
    return render_to_response('lifespan/factor_form.html', ctx,
        context_instance=RequestContext(request))


class FactorDetail(DetailView):
    model = Factor
    context_object_name = 'factor'
    template_name = 'lifespan/factor.html'
    #
    def get_context_data(self, **kwargs):
#        print("Get context data")
#        if 'symbol' in kwargs:
#            self.symbol = kwargs['symbol']
#            #kwargs['slug'] = self.symbol
#            del kwargs['symbol']
#        else:
#            self.symbol = None
        context = super(FactorDetail, self).get_context_data(**kwargs)
        if self.object.pdb: context['pdb'] = json.dumps(self.object.pdb.split(';')[0])
        else: context['pdb'] = None
        if self.object.entrez_gene_id:
            homolog = HomoloGene.objects.filter(entrez_gene_id=self.object.entrez_gene_id)[0]
            homologs = HomoloGene.objects.filter(hid=homolog.hid)
            orthologs = Ortholog.objects.filter(Q(gene=self.object.entrez_gene_id)|Q(ortholog=self.object.entrez_gene_id)).distinct()
         # Protein Ids:
            inparanoids = []
            proteins = gene2ensembl.objects.filter(entrez_gene_id=self.object.entrez_gene_id)
            #print(proteins)
            for protein in proteins:
                inparanoid_list = InParanoid.objects.filter(Q(ensembl_gene_id_a=protein.ensembl_protein_id)|Q(ensembl_gene_id_b=protein.ensembl_protein_id)).distinct()
                #print(inparanoid_list)
                for inparanoid in inparanoid_list:
                    inparanoids.append(inparanoid)
        elif self.object.ensembl_gene_id:
            inparanoids = []
            proteins = gene2ensembl.objects.filter(ensembl_gene_id=self.object.ensembl_gene_id)
            for protein in proteins:
                inparanoid_list = InParanoid.objects.filter(Q(ensembl_gene_id_a=protein.ensembl_protein_id)|Q(ensembl_gene_id_b=protein.ensembl_protein_id)).distinct()
                for inparanoid in inparanoid_list:
                    inparanoids.append(inparanoid)
        else:
            orthologs = ''
            homologs = ''
            inparanoids = ''
        context['orthologs'] = orthologs
        context['homologs'] = homologs
        context['inparanoids'] = inparanoids
        return context
#
    #def get_queryset(self):
        #print("Getting queryset")
#        if self.symbol:
#            qs = Factor.objects.filter(symbol__icontains=self.symbol)
#        else:
#            qs = Factor.objects.filter(pk=self.pk)
#        return qs

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return
        """
        #print("Get object")
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        slug = self.kwargs.get('slug', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            queryset = Factor.objects.filter(symbol=slug)
            #slug_field = self.get_slug_field()
            #queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's and error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either and object pk or a slug, you idiot!"
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        except MultipleObjectsReturned:
            for obj in queryset:
                if obj.symbol == slug:
                    return obj
        return obj


class CreateFactor(Create):
    model = Factor
    form_class = FactorForm
    comment = 'Created factor.'


"""Variants"""
def variants(request, pk):
    variant = Variant.objects.get(pk=pk)
    return render(request, 'lifespan/variant.html', {'variant': variant})

def add_variant(request):
    form = VariantForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with reversion.create_revision():
            variant = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = "Added variant. %s" % request.POST['comment'] or ''
            reversion.set_comment(comment)
            log(request, variant, comment)
            msg = "Successfully added variant."
            messages.add_message(request, messages.SUCCESS, ugettext(msg))
            return redirect('/lifespan/variant/%s' % variant.pk)
    ctx = {'form': form, 'action': 'Add'}
    return render(request, 'lifespan/variant_form.html', ctx)

@login_required
def edit_variant(request, pk):
    variant = Variant.objects.get(pk=pk)
    form = VariantForm(request.POST or None, instance=variant)
    if request.method == "POST" and form.is_valid():
        if "cancel" in request.POST:
            return redirect('/lifespan/variant/%s' % pk)
        with reversion.create_revision():
            form.save()
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Changed variant"
            reversion.set_comment(comment)
            log(request, variant, comment)
            return redirect('/lifespan/variant/%s' % pk)
    ctx = {'variant': variant, 'form': form, 'action': 'Edit'}
    return render(request, 'lifespan/variant_form.html', ctx)


class VariantDetail(DetailView):
    model = Variant
    context_object_name = 'variant'
    template_name = 'lifespan/variant.html'
    #
    def get_context_data(self, **kwargs):
#        print("Get context data")
#        if 'symbol' in kwargs:
#            self.symbol = kwargs['symbol']
#            #kwargs['slug'] = self.symbol
#            del kwargs['symbol']
#        else:
#            self.symbol = None
        context = super(VariantDetail, self).get_context_data(**kwargs)
        return context
#
    #def get_queryset(self):
        #print("Getting queryset")
#        if self.symbol:
#            qs = Factor.objects.filter(symbol__icontains=self.symbol)
#        else:
#            qs = Factor.objects.filter(pk=self.pk)
#        return qs

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return
        """
        #print("Get object")
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        slug = self.kwargs.get('slug', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            queryset = Variant.objects.filter(polymorphism=slug)
            #slug_field = self.get_slug_field()
            #queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's and error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either and object pk or a slug, you idiot!"
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        except MultipleObjectsReturned:
            for obj in queryset:
                if obj.polymorphism == slug:
                    return obj
        return obj


class VariantBulkInsert(FormView):
    template_name = 'lifespan/variant_bulk_insert.html'
    form_class = VariantBulkInsertForm
    success_url = '/lifespan/variants/'

    def form_valid(self, form):
        data = form.cleaned_data['data']
        keywords = ['curate', 'pmid', 'links', 'symbol', 'entrez', 'poylmporphism', 'shorter', 'odds', 'value', 'signficant', 'initial' , 'ethnicity', 'age', 'replication', 'type', 'notes']
        #print(data)
        headers = {}
        header = data.split('\n')[0]
        long_lived = False
        n = 1
        for head in header.split('\t'):
            print(head)
            if "onger" in head:
                long_lived = True
                n = 2

            if head in header: pass

        classification = Classification.objects.get(title="Longevity-Associated")
        no_age_effect = Classification.objects.get(title="No Age Effect")
        species = Species.objects.get(taxid=9606)
        assay = Assay.objects.get(name__startswith='Organi')

        # row-number -> ['value']
        # ['choice'] - row-number

        lines = data.split('\n')[1:]

        with reversion.create_revision():
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username="Anonymous")
            reversion.set_user(self.request.user)
            #comment = "Added factor. %s" % self.request.POST['comment'] or ''
            #reversion.set_comment(comment)
            #log(self.request, factor, comment)
            msg = "Successfully added variants."
            messages.add_message(self.request, messages.SUCCESS, ugettext(msg))
            for line in lines:
                created = False
                factors = []
                d = {}
                try:
                    notes = []
                    columns = line.replace('\r', '').split('\t')
                    #print(columns)
                    #print([name for name in columns[10].split(', ')])
                    # print("pmid", columns[1])
                    # print("entrez_gene_id", columns[4],Factor.objects.get_or_create(entrez_gene_id=columns[4]),
                    #       type(Factor.objects.get_or_create(entrez_gene_id=columns[4])))
                    # print("polymorphism", columns[5])
                    # print("shorter_lived_allele", columns[6])
                    # print("odds_ratio", columns[7])
                    # print("pvalue", columns[8])
                    # print("significant", columns[9])
                    # print("number_of_cases", columns[10])
                    # print("ethnicity", [columns[11]])
                    # print("age_of_cases", columns[12])
                    # print("technology", columns[13])
                    # print("study_type", columns[14])
                    # print("description", columns[15])



                    try:
                        choice = State.objects.get_or_create(name=columns[0])[0]
                        if choice: d.update({'choice':choice})
                    except Exception as e:
                        #print("choice", e)
                        choice = ''
                        notes.append("choice = %s (%s)" % (columns[0], e))
                    try:
                        pmid = int(columns[1].replace('N/A', ''))
                        if pmid: d.update({'pmid':pmid})
                    except Exception as e:
                        #print("pmid", e)
                        pmid = ''
                        notes.append("pmid = %s (%s)" % (columns[1], e))
                    try:
                        if columns[4]:
                            factor, created = Factor.objects.get_or_create(entrez_gene_id=columns[4], symbol=columns[3], species=species) #& Q(taxid=9606)
                        else:
                            factor, created = Factor.objects.get_or_create(symbol=columns[3], species=species) #& Q(taxid=9606)
                        if factor:
                            print("Get or created factor: %s %s" % (factor, created))
                            significancy = columns[n+8].lower()
                            if 'yes' in significancy:
                                observation = ' was found to be associated with longevity [%s]. ' % pmid
                                if not observation in factor.observation:
                                    factor.observation += columns[3] + observation
                                factor.classifications.add(classification)
                            elif 'no' in significancy:
                                observation = ' was not found to be associated with longevity [%s]. ' % pmid
                                if observation not in factor.observation:
                                    factor.observation += columns[3] + observation
                                factor.classifications.add(no_age_effect)
                            factor.assay.add(assay)
                            print(factor.classification)
                            factor.save()
                            #print("Found factor: %s" % factor)
                            factors.append(factor)
                            print("Created factor")
                        if factor: d.update({'factor':factor})
                    except Exception as e:
                        #print("factor", e)
                        factor = ''
                        if columns[4] != "N/A" or (columns[3] or columns[4]):
                            notes.append("gene symbol = %s (%s)" % (columns[3], e))
                            notes.append("entrez gene id = %s (%s)" % (columns[4], e))
                    try:
                        polymorphism = columns[5].replace('N/A', '')
                        if polymorphism: d.update({'polymorphism':polymorphism})
                    except Exception as e:
                        #print("polymorphism", e)
                        polymorphism = '-'
                        notes.append("polymorphism = %s (%s)" % (columns[5], e))
                    if polymorphism == '':
                        polymorphism = '-'
                        d.update({'polymorphism':polymorphism})
                    try:
                        shorter_lived_allele = columns[6].replace('N/A', '')
                        if shorter_lived_allele: d.update({'shorter_lived_allele':shorter_lived_allele})
                    except Exception as e:
                        #print("shorter_lived_allele", e)
                        shorter_lived_allele = ''
                        notes.append("shorter_lived_allele = %s (%s)" % (columns[6], e))
                    if long_lived:
                        try:
                            longer_lived_allele = columns[7].replace('N/A', '')
                            if longer_lived_allele: d.update({'longer_lived_allele': longer_lived_allele})
                        except Exception as e:
                            #print("shorter_lived_allele", e)
                            longer_lived_allele = ''
                            notes.append("longer_lived_allele = %s (%s)" % (columns[7], e))

                    try:
                        if columns[n+6] != 'N/A' and columns[n+6] != 'NA' and columns[n+6] != '':
                            odds_ratio = float(columns[n+6])
                        else: #rs1042719
                            odds_ratio = None
                        if odds_ratio: d.update({'odds_ratio':odds_ratio})
                    except Exception as e:
                        odds_ratio = ''
                        notes.append("odds_ratio = %s (%s)" % (columns[n+6], e))
                    try:
                        if columns[n+7] == 'NS':
                            pvalue = 1
                            p_value = 'NS'
                        elif columns[n+7] != 'N/A' and columns[n+7]:
                            p_value = columns[n+7]
                            d.update({'p_value': p_value})
                            pvalue = float(columns[n+7].replace('x', '*').replace('*10^', 'E').replace('*10**', 'E').replace('=', '').replace(' ', '').replace('P', '').replace('p', '').replace('>', '').replace('<', '').replace(',', ''))
                        else:
                            pvalue = None
                            p_value = None
                        if pvalue: d.update({'pvalue':pvalue})
                        if p_value: d.update({'p_value': p_value})
                    except Exception as e:
                        #print("odds ratio", e)
                        pvalue = ''
                        notes.append("pvalue = %s (%s)" % (columns[n+7], e))
                        if p_value: d.update({'p_value': p_value})
                    try:
                        significant = columns[n+8].replace('N/A', '')
                        if significant: d.update({'significant':significant})
                    except Exception as e:
                        #print("significant", e)
                        significant = ''
                        notes.append("significant = %s (%s)" % (columns[n+8], e))
                    try:
                        initial_number = columns[n+9].replace('N/A', '')
                        if initial_number: d.update({'initial_number':initial_number})
                    except Exception as e:
                        #print("initial number", e)
                        initial_number = ''
                        notes.append("initial number = %s (%s)" % (columns[n+9], e))
                    try:
                        ethnicity = columns[n+10].replace('N/A', '')
                        #if ethnicity: d.update({'ethnicity':ethnicity})
                    except Exception as e:
                        #print("ethnicity", e)
                        ethnicity = ''
                        #notes.append("ethnicity = %s (%s)" % (columns[11], e))
                    try:
                        age_of_cases = columns[n+11].replace('N/A', '')
                        if age_of_cases: d.update({'age_of_cases':age_of_cases})
                    except Exception as e:
                        #print("age of cases", e)
                        age_of_cases = ''
                        notes.append("age of cases = %s (%s)" % (columns[n+11], e))
                    try:
                        replication_number = columns[n+12].replace('N/A', '')
                        if replication_number: d.update({'replication_number':replication_number})
                    except Exception as e:
                        #print("replication_number", e)
                        replication_number = ''
                        notes.append("replication_number = %s (%s)" % (columns[n+12], e))

                    try:
                        print('technology: %s' % columns[n+13])
                        technology = Technology.objects.get_or_create(name=columns[n+13])[0]
                        if technology: d.update({'technology':technology})
                        print("Technology was successfully applied.")
                    except Exception as e:
                        print("technology", e)
                        technology = ''
                        #notes.append("technology = %s (%s)" % (columns[13], e))
                    try:
                        print('study type: %s' % columns[n+14])
                        study_type = StudyType.objects.get_or_create(name=columns[n+14])[0]
                        print("Study type is %s %s" % (str(study_type), study_type))
                        if study_type: d.update({'study_type':study_type})
                    except Exception as e:
                        print("study type", e)
                        study_type = ''
                        notes.append("study type = %s (%s)" % (columns[n+14], e))
                    try:
                        print("Description: %s" % columns[n+15])
                        description = columns[n+15].replace('N/A', '')
                        if description: d.update({'description':description})
                    except Exception as e:
                        #print("description", e)
                        description = ''
                        #notes.append("description = %s (%s)" % (columns[15], e)
                    try:
                        print("References: %s" % columns[1])
                        reference = Reference.objects.get_or_create(pmid=columns[1])[0]
                        if reference: d.update({'reference':reference})
                    except Exception as e:
                        print("reference", e)
                        reference = ''
                        #notes.append("reference = %s (%s)" % (columns[1], e))
                    try:
                        print("Finding: %s" % columns[n+16])
                        choices = {'Positive': 1, 'Negative': 2}
                        finding = choices[columns[n+16]]
                        if finding: d.update({'finding': finding})
                    except Exception as e:
                        finding = ''
                        notes.append("finding = %s (%s)" % (columns[n+16], e))
                        print("16 %s" % columns[n+16])
                    try:
                        print("Variant type: %s" % columns[n+17])
                        variant_type = VariantType.objects.get_or_create(name=columns[n+17])[0]
                        print("Fetched variant type: %s" % str(variant_type))
                        if variant_type: d.update({'variant_type': variant_type})
                    except Exception as e:
                        variant_type = None
                        print("17 %s" % columns[n+17])
                        notes.append("variant type = %s (%s)" % (columns[n+17], e))
                    print(len(columns), n+18)
                    if len(columns) > n+18:
                        print("Trying")
                        print  columns[n+18]
                        try:

                            print("OR type: %s" % columns[n+18])
                            or_type = ORType.objects.get_or_create(name=columns[n+18])[0]
                            if or_type: d.update({'or_type': or_type})
                        except Exception as e:
                            or_type = None
                            notes.append("or type = %s (%s)" % (columns[n+18], e))
                        #print("18 %s" % columns[n+18])


                    if 'description' in d:
                        d['description'] = d['description'] + '\n\n'+'\n\n'.join(notes)
                    else:
                        d.update({'description':  '\n\n'.join(notes)})
                    variant = Variant.objects.create(**d) #choice=choice,
                                           # pmid=pmid,
                                           # factor=factor,
                                           # polymorphism=polymorphism,
                                           # shorter_lived_allele=shorter_lived_allele,
                                           # odds_ratio=odds_ratio,
                                           # pvalue=pvalue,
                                           # significant=significant,
                                           # initial_number=initial_number,
                                           # age_of_cases=age_of_cases,
                                           # technology=technology,
                                           # study_type=study_type,
                                           # description=description,
                                           # reference=reference)
                    ethnicity = [Population.objects.get_or_create(name=population)[0] for population in ethnicity.replace(';', ',').replace(', ', ',').split(',')]
                    for e in ethnicity:
                        variant.ethnicity.add(e)
                        #variant.save()
                    if created:
                        variant.factor = factor
                        variant.factors.add(factor)
                        #variant.save()
                    for f in factors:
                        variant.factors.add(f)
                        #variant.save()
                    if 'yes' in significant.lower():
                        variant.classifications.add(classification)
                    else:
                        variant.classifications.add(no_age_effect)
                    variant.save()
                    messages.add_message(self.request, messages.SUCCESS, "%s" % (line))
                except Exception as e:
                    messages.add_message(self.request, messages.ERROR, "%s %s" % (e, line))
                    print(e)

        return super(VariantBulkInsert, self).form_valid(form)


class CreateVariant(Create):
    model = Variant
    form_class = VariantForm
    comment = 'Created variant.'
    message = 'Successfully created %s'

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



class VariantList(SingleTableView, FormView):
    template_name = 'lifespan/variants.html'
    context_object_name = 'variants'
    table_class = VariantTable
    form_class = FilterForm
    success_url = '/lifespan/variants/'
    model = Variant
    query = None
    symbol = None
    variants = None
    output = False
    chromosome = None
    chromosome_number = None
    term = None
    sql = None
    count = 0
    #
    # def get(self, request, *args, **kwargs):
    #     VariantList.query = None
    #     VariantList.symbol = None
    #     VariantList.variants = None
    #     VariantList.output = False
    #     VariantList.chromosome = None
    #     return super(VariantList, self).get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        print("Dispatch")
        #VariantList.count += 1
        print("Variant count is %s" % VariantList.count)
        #VariantList.query = None
        #VariantList.term = None
        #print("outer")
        #print(args, kwargs)
        if 'chromosome' in kwargs:
            #print(kwargs['chromosome'])
            #print("inner")
            VariantList.chromosome_number = kwargs['chromosome']
        # print('kwargs/output %s' % kwargs['output'])
        # if 'output' in kwargs:
        #     if kwargs['output'] == 'output':
        #         self.download = True
        #     else:
        #         self.download = False
        # print("Output %s" % self.download)
        return super(VariantList, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print("Form valid is triggered")
        # print(VariantList.variants)

        VariantList.query = form.cleaned_data['filter']
        VariantList.term = form.cleaned_data['term']
        VariantList.chromosome = form.cleaned_data['chromosome']
        output = form.cleaned_data['output']
        self.output = output
        VariantList.output = output
        #print(output)
        # print(VariantList.term)
        if VariantList.term:
            print("Variant list term is true")
            term = VariantList.term.replace('"', '')
            if 'GO:' in VariantList.term:
                terms = GO.objects.filter(go_id=term)
            else:
                terms = GO.objects.filter(go_term__icontains=term)
            ids  = ["Q(factor__entrez_gene_id=%s)" % go.entrez_gene_id for go in terms]
            #print(ids)
            VariantList.sql = " | ".join(ids)
            variants = eval("Variant.objects.filter("+self.sql+")")
            self.kwargs['variants'] = variants
            if not VariantList.variants:
                 VariantList.variants = variants
        #FactorList.symbol = form.cleaned_data['symbol']
        return super(VariantList, self).form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid is triggered")
        # print(VariantList.variants)

        VariantList.query = None
        VariantList.term = None
        #print self.variants
        return super(VariantList, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        print("Get context data is triggered")
        # print(VariantList.variants)
        VariantList.count += 1
        context = super(VariantList, self).get_context_data(*args, **kwargs)
        context['form'] = FilterForm() #initial={'filter': VariantList.query, 'term':VariantList.term}
        context['variantsfilter'] = self.variantsfilter
        context['entry'] = get("Lifespan Variants")
        # print("Get context data")
        # print self.variants
        # print("Variants in %s" % 'variants' in self.kwargs)
        # if 'variants' in self.kwargs:
        #     print("Variants %s" % self.kwargs['variants'])

        # print("Chromosome: %s" % self.chromosome)
        # if VariantList.chromosome and self.queryset:
        #     if VariantList.chromosome == 'X' or VariantList.chromosome == 'Y':
        #         self.queryset.filter(location=self.chromosome)
        #     else:
        #         self.queryset.filter(Q(location__startswith=self.chromosome+'q')|Q(location__startswith=self.chromosome+'p'))
        # print self.queryset
        return context

    def render_to_response(self, context, **response_kwargs):
        print("Render to response")
        VariantList.sql = None
        if VariantList.output: # or self.download:
            VariantList.output = False
            if self.request.user.is_authenticated():
                 #print(len(self.qs))
                 #print(self.queryset)
                 #print(len(self.object_list))
                 #print(len(self.variantsfilter.qs))
                 response = HttpResponse(content_type='text/csv')
                 response['Content-Disposition'] = 'attachment: filename="output.csv"'
                 writer = csv.writer(response, delimiter="\t")
                 dump(self.object_list, write=False, writer=writer)
                 return response
            else:
                return redirect(settings.LOGIN_URL)
        else:
            return super(VariantList, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        print("Get queryset is triggered")
        print(VariantList.variants)

        if VariantList.query:
            #VariantList.variants = None
            try:
                query = float(VariantList.query)
                variants = Variant.objects.filter(Q(odds_ratio=query) |
                                                Q(pvalue=query) |
                                                Q(pmid=query) |
                                                Q(factor__entrez_gene_id=query))
            except Exception as e:
                variants = Variant.objects.filter(Q(polymorphism__icontains=VariantList.query) |
                                             Q(location__icontains=VariantList.query) |
                                             Q(initial_number__icontains=VariantList.query) |
                                             Q(replication_number__icontains=VariantList.query) |
                                             Q(age_of_cases__icontains=VariantList.query) |
                                             Q(factor__symbol=VariantList.query) |
                                             Q(factor__name__icontains=VariantList.query) |
                                             Q(factor__ensembl_gene_id=VariantList.query) |
                                             Q(description__icontains=VariantList.query) |
                                             Q(longer_lived_allele__icontains=VariantList.query) |
                                             Q(shorter_lived_allele__icontains=VariantList.query) |
                                             Q(ethnicity__name__icontains=VariantList.query) |
                                             Q(study_type__name__icontains=VariantList.query) |
                                             Q(technology__name__icontains=VariantList.query) |
                                             Q(reference__title__icontains=VariantList.query)).order_by('-id').order_by('pvalue')
        else:
            variants = Variant.objects.all().order_by('pvalue').exclude(pvalue=None) #, 'longer_lived_allele')
        # if (not VariantList.query and not VariantList.symbol and not VariantList.variants and not VariantList.sql) and self.request.method == 'GET':
        #     print('got it')
        #     variants = Variant.objects.all().order_by('pvalue').exclude(pvalue=None)
        self.variantsfilter = VariantFilterSet(variants, self.request.GET)
        #if self.variants:
        #    return self.variants
        #else:


        self.qs = self.variantsfilter.qs.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
        print(len(self.qs))




        #     print("VariantList.variants: %s" % VariantList.variants)
        #     variants = VariantList.variants
        #     # print(variants)
        #     #VariantList.variants = None
        #     return variants
        # # if 'variants' in self.kwargs:
        # #     print("Variants %s" % self.kwargs['variants'])
        #print("variantsfilter")


        print("Chromosome: %s" % self.chromosome)
        print(VariantList.chromosome)
        print("Number %s" % VariantList.chromosome_number)
        if VariantList.chromosome_number:
            if VariantList.chromosome_number == 'MT':
                self.qs = self.qs.filter(Q(location__startswith='MT'))
            else:
                self.qs = self.qs.filter(Q(location__startswith=str(VariantList.chromosome_number)+'q')|
                Q(location__startswith=str(VariantList.chromosome_number)+'p'))

        if VariantList.chromosome:
            chromosomes = ["Q(location__startswith='%sq')|Q(location__startswith='%sp')" % (c,c)
                           for c in VariantList.chromosome if c not in ['X', 'Y']]
            if 'X' in VariantList.chromosome:
                #self.qs.filter(location=self.chromosome)
                chromosomes.append("Q(location__icontains='X')")
            if 'Y' in VariantList.chromosome:
                chromosomes.append("Q(location__icontains='Y')")
            if 'MT' in VariantList.chromosome:
                chromosomes.append("Q(location__icontains='MT')")
            print(chromosomes)
            self.qs = eval("self.qs.filter("+'|'.join(chromosomes)+")")
            #VariantList.chromosome = False
        print("Filtering")
        if VariantList.variants and VariantList.sql:
            #print(VariantList.sql)
            variants = eval("self.qs.filter("+VariantList.sql+")")
            self.qs = variants
            #VariantList.sql = None
            #print(len(variants))
            #VariantList.variants = None
            return variants

        print("Variantlist count = %s" % VariantList.count)
       # if VariantList.count = 2:
        if VariantList.count == 1:
            VariantList.count = 0
            VariantList.query = None
            VariantList.term = None

        return self.qs


class VariantView(object):
    form_class = VariantForm
    model = Variant


class VariantDelete(Delete):
    model = Variant
    comment = 'Deleted variant'
    success_url = reverse_lazy('variants')
    message = 'Successfully deleted %s'

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

@login_required
def remove_variant(request, pk):
    variant = Variant.objects.get(pk=pk)
    variant.delete()
    msg = 'Successfully removed %s' % variant
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/lifespan/')


class VariantIssues(ListView):
    model = Variant
    template_name = 'lifespan/variant_issues.html'
    queryset=Variant.objects.filter(pvalue=None).exclude(choice__name__contains='Review')
    def get_context_data(self, **kwargs):
        context = super(VariantIssues, self).get_context_data(**kwargs)
        ids = [(obj.reference, obj) for obj in self.queryset]
        dict = {}
        for reference, obj in ids:
            if reference not in dict:
                dict[reference] = [obj]
            else:
                dict[reference].append(obj)
        context['pmids'] = dict
        #print context['pmids']
        return context


class VarianceDetail(ListView):
    model = Variant
    template_name = 'lifespan/variant_detail.html'

    def dispatch(self, request, **kwargs):
        #print("Dispatch")
        self.name = kwargs['name']
        #print(self.name)
        return super(VarianceDetail, self).dispatch(request, **kwargs)

    def get_context_data(self, **kwargs):
        #print("Get context data")
        context = super(VarianceDetail, self).get_context_data(**kwargs)
        context['variant'] = self.name
        context['variants'] = Variant.objects.filter(polymorphism__icontains=self.name)
        #print(context['variants'])
        return context


class ManipulationDetail(DetailView):
    model=Manipulation
    context_object_name = 'manipulation'
    template_name = 'lifespan/manipulation.html'

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return
        """
        #print("Get object")
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
            # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        slug = self.kwargs.get('slug', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            queryset = Manipulation.objects.filter(shortcut__iexact=slug)
            #slug_field = self.get_slug_field()
            #queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's and error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either and object pk or a slug, you idiot!"
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class FactorList(SingleTableView, FormView):
    template_name = 'lifespan/factors.html'
    context_object_name = 'factors'
    table_class = FactorTable
    form_class = FilterForm
    success_url = '/lifespan/factors/'
    model = Factor
    query = None
    symbol = None

    def form_valid(self, form):
        FactorList.query = form.cleaned_data['filter']
        #FactorList.symbol = form.cleaned_data['symbol']
        return super(FactorList, self).form_valid(form)

    def form_invalid(self, form):
        FactorList.query = None
        return super(FactorList, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(FactorList, self).get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={'filter': FactorList.query})
        context['factorsfilter'] = self.factorsfilter
        context['entry'] = get("Factor")
        return context

    def get_queryset(self):
        #if FactorList.symbol:
        #   factors = factors.filter(symbol=FactorList.symbol)
        if FactorList.query:
            factors = Factor.objects.filter(Q(symbol__icontains=FactorList.query) |
                                         Q(name__icontains=FactorList.query) |
                                         Q(ensembl_gene_id=FactorList.query) |
                                         Q(observation__icontains=FactorList.query) |
                                         Q(note__icontains=FactorList.query)).order_by('-id')
        else:
            factors = Factor.objects.all().order_by('-id')
        self.factorsfilter = FactorFilterSet(factors, self.request.GET)
        return self.factorsfilter.qs


class FactorView(object):
    form_class = FactorForm
    model = Factor


class FactorDelete(Delete):
    model = Factor
    comment = 'Deleted factor'
    success_url = reverse_lazy('factors')


def epistasis(request):
    entry = get(title='Epistasis of Longevity')
    data = entry.text.split('\n')
    description = data[0]
    pmids = [i for i in data[2:] if i]
    ctx = {'entry': entry, 'description': description, 'pmids': pmids}
    return render_to_response('lifespan/epistasis.html', ctx,
        context_instance=RequestContext(request))

def regimen(request, pk):
    regimen = Regimen.objects.get(pk=pk)
    return render_to_response('lifespan/regimen.html', {'regimen': regimen},
        context_instance=RequestContext(request))

def manipulations(request):
    return HttpResponse("manipulations")

def manipulation(request, pk):
    return HttpResponse("manipulation")

def assays(request):
    return HttpResponse("assays")

def assay(request, pk):
    return HttpResponse("assay")

def type(request):
    return HttpResponse("type")


class CreateStrain(Create):
    model = Strain
    form_class = StrainForm
    comment = 'Created strain.'


class UpdateStrain(Update):
    model = Strain
    form_class = StrainForm
    comment = 'Updated strain.'


def newIntervention(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, InterventionForm, 'intervention')

def newFactor(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, FactorForm, 'factor')

def newChoice(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, StateForm, 'state')

def newPopulation(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, PopulationForm, 'population')

def newTechnology(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, TechnologyForm, 'technology')

def newStudyType(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, StudyTypeForm, 'study_type')

def newVariantType(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, VariantTypeForm, 'variant_type')

def newORType(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, ORTypeForm, 'or_type')

#234567891123456789212345678931234567894123456789512345678961234567897123456789

def correct_classes(request):
    """Performs automated correction of the factor classifications."""
    from annotations.models import Classification
    gerontogene = Classification.objects.get(title='Gerontogene')
    agingSuppressor = Classification.objects.get(title='Aging-Suppressor')

    factors = Factor.objects.filter(Q(classifications__title='Positive Gerontogene') |
                                    Q(classifications__title='Negative Gerontogene'))
    msg = 'Gerontogenes: %s' % factors.count()
    #print(msg)
    messages.add_message(request, messages.SUCCESS, msg)
    for factor in factors:
        factor.classifications.add(gerontogene)

    factors = Factor.objects.filter(Q(classifications__title='Positive Aging-Suppressor') |
                                    Q(classifications__title='Negative Aging-Suppressor'))
    msg = 'Aging-Suppressors: %s' % factors.count()
    messages.add_message(request, messages.SUCCESS, msg)
    print(msg)
    for factor in factors:
        factor.classifications.add(agingSuppressor)
    return redirect("lifespan")



def describe(request):
    """Annotates the AgeFactor table with description from various sources.
    Put everything into a seperate thread."""
    from Annotations import Annotation

    print("Restrict to genes for now:")
    factors = Factor.objects.filter(entrez_gene_id__isnull=False)
    all = Factor.objects.all()
    print len(factors), len(all)

    # Get a dict of all entrez ids:
    ids = [factor.entrez_gene_id for factor in factors]
    # Pass it to Annotation:
    genes = Annotation.describe(ids)

    for factor in factors:
        if factor.entrez_gene_id in genes:
            #try:
            factor.description = genes[factor.entrez_gene_id].description or ''
            #factor.description.replace(r"\xCE\xB1", 'alpha').replace(r"0xce", '')
            #factor.description.encode('utf-8')
            #except:
                #pass
            #
        #print factor.description
            factor.save()
        else: print factor.entrez_gene_id, factor.symbol, factor.name
    print "Done"
    
    return HttpResponse('Description function works!')

def isdigit(num):
    try: return int(num)
    except: return False

def functional_description(request):
    """Unites the function and description fields."""   
    import re
    p = '\D\D\D; \D\D\D' # non pmid boundaries
    def repl(string):
        string = string.group(0)
        string = string.replace('; ', '##')
        return string
    
    count = 0
    genes = Factor.objects.all()
    for gene in genes:

        
        functions = re.sub(p, repl, gene.function)
        functions = functions.split('##')

        #description = gene.description
        
        descriptions = gene.description.split('; ')
        described = False
        for descr in descriptions:
            if descr.endswith('[UniProt]'):
                description = descr
                described = True
                break
        if not described:
            description = '; '.join(descriptions)
        descriptions = set(description.split(' '))
            
        for function in functions:
            if isdigit(function[:-3]) or isdigit(function[:3]): continue # ignore pmids
            terms = set(function.split(' '))
            intersection = terms.intersection(descriptions)
            if intersection and len(intersection) < len(terms)*0.4:
                gene.functional_description = function+'; '+description
                count += 1
            else:
                if gene.description:
                    gene.functional_description = description
                else:
                    gene.functional_description = gene.function
        gene.save()
    return HttpResponse('%s functions and description united.' % count)



class FactorOntology(FormView):
    form_class = OntologyForm
    template_name='lifespan/ontology.html'
    success_url= '/lifespan/factor/ontology'
    table = None

    def get_context_data(self, *args, **kwargs):
        context = super(FactorOntology, self).get_context_data(*args, **kwargs)
        context['result'] = FactorOntology.table
        return context

    def form_valid(self, form):
        classifications = form.cleaned_data['classifications']
        species = form.cleaned_data['species']
        types = form.cleaned_data['types']
        statement = []
        factors = []
        for s in species:
            statement.append('Q(species=%s)' % s.pk)
        species_query = ' | '.join(statement)
        statement = []
        #print(species_query)
        for c in classifications:
            statement.append('Q(classifications=%s)' % c.pk)
        classifications_query = ' | '.join(statement)
        if classifications:
            factors = eval('Factor.objects.filter((' + species_query + ') & ' + classifications_query+')')
        else:
           factors = eval('Factor.objects.filter(' + species_query + ')')
        statement = []
        #print(species_query)
        for t in types:
            statement.append('Q(types=%s)' % t.pk)
        type_query = ' | '.join(statement)

        #print(type_query)
        if type_query:
            factors = eval('factors.filter(' + type_query + ')')
       # print(len(factors))
        #print(factors)

        # for organism in species:
        #     print organism
        #     query = Factor.objects.filter(species=organism)
        #     for classification in classifications:
        #         print(classification)
        #         query = query.filter(classifications=classifications)
        #         f  = [factor.entrez_gene_id for factor in query]
        #         print(len(f))
        #         factors.extend(f)#, types=types)
        #print(factors)

        if factors: FactorOntology.table = functional_enrichment(True, [factor.entrez_gene_id for factor in factors])
        return super(FactorOntology, self).form_valid(form)


def integrity(request):
    """Checks for the quality of database records.
    e.g. are all annotations up to date, no naming conflicts.
    no duplicates, etc."""

    factors = Factor.objects.exclude(intervention__manipulation__shortcut='DT') #(filter(~Q)
    taxids = []
    ids = []
    dups = duplicates("Factor")
    noclasses = []
    nointervention = []

    for factor in factors:

        # Missing Taxonomy identifier:
        if not factor.taxid:
            taxids.append(factor)

        # Missing primary id:
        if not factor.entrez_gene_id and factor.symbol not in ['CKIepsilon', 'cyc1', 'Y46G5A.6']:
            #missed = '\t'.join(map(str, [factor.entrez_gene_id, factor.symbol,

            #if factor.symbol:print m(factor.symbol, factor.taxid)
            #print missed
            #print type(m), type(factor.symbol), type(factor.taxid)
            synonyms =[]
            factor.alias = set()
            if factor.symbol:
                synonyms.append(str(factor.symbol))
            if factor.name:
                synonyms.append(str(factor.name))
            try:
                mapped = m(synonyms, factor.taxid)
                factor.id = mapped[0]
                factor.ensembl = mapped[1]['ensembl_gene']
                for k,v in mapped[1].items():
                    if isinstance(v, list):
                        continue
                        for i in v:
                            factor.alias.add(i)
                    else:
                        factor.alias.add(v)
            except Exception as e:
                print e, factor
            factor.alias = '; '.join(list(map(str, factor.alias)))

            #factor.mapped = mapped

            ids.append(factor)

        # Are all genes classified?
        #print factor.classifications.all()
        try:
            if not factor.classifications.all():
                #print factor.symbol, "has no classification associated."
                noclasses.append(factor)
        except Exception as e:
            print e, factor.id, factor.symbol, "failed"

        # Links to interventions:
        try:
            if not factor.intervention.all():
                #print factor.symbol, "is not linked to an intervention"
                nointervention.append(factor)
        except Exception as e:
            print e, factor.id, factor.symbol, "failed"
    #print len(noclasses), "Unclassified."
    #print len(nointervention), "without an intervention associated."
    nc = set([factor.entrez_gene_id for factor in noclasses])
    ni = set([factor.entrez_gene_id for factor in nointervention])
    intersection = nc & ni
    print "Intersection: ", len(intersection)
    ctx = {'taxids': taxids,
           'ids': ids,
           'dups': dups,
           'noclasses': noclasses
    }
    return render_to_response('lifespan/integrity.html', ctx,
        context_instance=RequestContext(request))

def map_species(request, model):
    models = eval(model.title()+'.objects.all()')
    species = dict([(s.taxid,s) for s in Species.objects.all()])
    mapped = 0
    for m in models:
        if m.taxid in species:
            m.species = species[m.taxid]
            mapped += 1
            m.save()
        else:
            print m.name, m.taxid
    msg = 'Mapped %s species' % mapped
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/lifespan/')

def duplicates(model):
    """Identifies duplicates entries in a tablevbased on unique identifiers
    (i.e. entrez gene IDs)."""
    ids = {}
    dups = []
    records = eval(model+'.objects.all()')
    for record in records:
        id = record.entrez_gene_id
        if id:
            if id in ids:
                dups.extend([record, ids[id]])
                print id
            else: ids[id] = record
    return dups

def replace(request, table, field, term, by):
    """Replaces a string in a filed by another string."""
    print request, field, term, by
    records = eval(table+'.objects.all()')
    pre = []
    post = []
    result  = ''
    for record in records:
        attr = getattr(record, field)
        if term in attr:
            print
            print record.id
            print attr
            print
            pre.append(attr)
            mod_attr = attr.replace(term, by)
            print mod_attr
            post.append(mod_attr)
            setattr(record, field, mod_attr)
            print #getattr(record, field)
            record.save()
    for index, string in enumerate(pre):
        result += '\n'.join([pre[index]+'\n'+post[index]])#
    return HttpResponse("Replace in table %s field %s the term %s by %s\n%s" % (table, field, term, by, result))

def dumper(request):
    """Dumps information from GenAge out to a file (GenDR by default)."""
    import re
    from scripts.c import multiple_replace
    
    output = open("GenDR.txt", 'w')
    output.write("\t".join(["entrez_gene_id", "ensembl_gene_id", "taxid", "symbol", "name", "alias", "function", "description", "functional_description", "observation", "regimens", "lifespans", "references"])+'\n') #"classifications", 
    #genes = Factor.objects.all()
    genes = Factor.objects.filter(classifications__shortcut='DE')
    print len(genes)
    for gene in genes:
        #classifications = gene.classifications.all()
        #classes = []
        #for classification in classifications:
         #classes.append(classification.shortcut)
        regimens = gene.regimen.all()
        regimes = []
        for regimen in regimens:
         regimes.append(regimen.shortcut)
        aliases = gene.alias.replace(';', '; ')
        lifespan = gene.lifespan.all()
        lifespans = [ls.shortcut for ls in lifespan]
        if ("Geber et al., unpublished" not in gene.reference and "Tang et al., unpublished" not in gene.reference): #"DE" in classes and
          
            description = gene.description #decode('utf-8')
            description = description.replace(u'β','Beta')
            if description:
                description = description.encode('utf-8') #[0]
            functional_description = gene.functional_description
            functional_description = functional_description.replace(u'β','Beta')

            references = set()
            pattern = '\[(.+?)\]'
            findings = re.findall(pattern, str(gene.observation))
            for finding in findings:
                items = finding.replace('; ', ';').split(';')
                for item in items:
                    print item
                    references.add(item)
            
            try:
                output.write("\t".join(map(str, [gene.entrez_gene_id,
                                                     gene.ensembl_gene_id,
                                                     gene.taxid,
                                                     gene.symbol,
                                                     gene.name,
                                                     aliases,
                                                     gene.function,
                                                     description,
                                                     functional_description.encode('utf-8'),
                                                     multiple_replace(gene.observation, {'\n':' ','\r':' '}),
                                                     #"; ".join(classes),
                                                     "; ".join(regimes),
                                                     "; ".join(lifespans),
                                                     "; ".join(references)])) +'\n'    )         
            except:
                print "gene symbol:", gene.symbol
                print gene.description
                print gene.functional_description
                #
                print
    print "done"
    return HttpResponse("GenDR was successfully saved.")

def annotate_chromosomal_locations(verbose=True):
    errors = []
    variants = Variant.objects.all()
    for variant in variants:
        if not variant.location:
            locations = []
            factors = variant.factors.all()
            if factors:
                for factor in factors:
                    if factor.entrez_gene_id:
                        try:
                            handle = Entrez.efetch(db='gene', id=factor.entrez_gene_id, format='xml')
                            record = Entrez.read(handle)
                            #print(record.keys())
                            #print(handle.read())
                            location = record[0]['Entrezgene_location'][0]['Maps_display-str']
                            if verbose:
                                print("Gene: %s %s" % (factor.entrez_gene_id, location)) #19p13.3-p13.2
                            if location not in locations:
                                locations.append(location)
                        except Exception as e:
                            errors.append(e)
            variant.location = "; ".join(locations)
            variant.save()
            if verbose:
                print("Variant: %s %s\n" % (variant, variant.location))
    if errors:
        print("Errors: %s" % len(errors))
    for index, error in enumerate(errors):
        print("%: %s" % (index, error))

def annotate_locations(request):
    annotate_chromosomal_locations(verbose=False)
    return redirect('variants')

##      elif  "DE" in classes:
##         print gene.symbol, gene.reference

#dump()
#stop

# Kept for reference:
#@login_required
#def edit_experiment(request, pk):
#    experiment = Experiment.objects.get(pk=pk)
#    form = ExperimentForm(request.POST or None, instance=experiment)
#    if request.method == "POST" and form.is_valid():
#        form.save()
#        return redirect('lifespan/experiment/%s' % pk)
#    ctx = {'experiment': experiment, 'form': form}
#    return render_to_response('lifespan/edit_experiment.html', ctx,
#        context_instance=RequestContext(request))


