# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
#from django.core.urlresolvers import reverse # reverse_lazy (Django 1.4)
from django.contrib.auth.models import AnonymousUser, User
from django.views.generic.edit import CreateView, UpdateView, FormView # DeleteView
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

import reversion

from django_tables2 import SingleTableView, RequestConfig

from models import (Study, Experiment, Measurement, Comparison, Intervention, Factor, Regimen, Strain,
                   Manipulation)
from forms import (StudyForm, EditStudyForm, DeleteStudyForm,
                   ExperimentForm, DeleteExperimentForm,
                   ComparisonForm,
                   InterventionForm, DeleteInterventionForm, InterventionFilterSet,
                   FactorForm, StrainForm,
                   FilterForm, FactorFilterSet)
from tables import ComparisonTable, InterventionTable, FactorTable

from blog.models import Post
from annotations.models import Species

from meta.view import log
from home.views import LoginRequiredMixin
from data.views import Create, Update, Delete
from data import get


def index(request):
    lifespan = Post.objects.get(title="Lifespan")
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
    try: experiments_entry = Post.objects.get(title="Experiments")
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
                                                       Q(effect__icontains=InterventionList.query))
        else:
            interventions = Intervention.objects.all()
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
#    def get_context_data(self, **kwargs):
#        print("Get context data")
#        if 'symbol' in kwargs:
#            self.symbol = kwargs['symbol']
#            #kwargs['slug'] = self.symbol
#            del kwargs['symbol']
#        else:
#            self.symbol = None
#        context = super(FactorDetail, self).get_context_data(**kwargs)
#        return context
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
        return context

    def get_queryset(self):
        #if FactorList.symbol:
        #   factors = factors.filter(symbol=FactorList.symbol)
        if FactorList.query:
            factors = Factor.objects.filter(Q(symbol__icontains=FactorList.query) |
                                         Q(name__icontains=FactorList.query) |
                                         Q(ensembl_gene_id=FactorList.query) |
                                         Q(observation__icontains=FactorList.query) |
                                         Q(note__icontains=FactorList.query))
        else:
            factors = Factor.objects.all()
        self.factorsfilter = FactorFilterSet(factors, self.request.GET)
        return self.factorsfilter.qs


class FactorView(object):
    form_class = FactorForm
    model = Factor


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


#234567891123456789212345678931234567894123456789512345678961234567897123456789

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
    return HttpResponse('%s functions and discription united.' % count)

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

def dump(request):
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


