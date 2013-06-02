# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.db.models import Q
from django.contrib.auth.models import User, AnonymousUser
from django_tables2 import SingleTableView

from forms import  FilterForm, UploadForm, ReferenceForm
from tables import ReferenceTable
from filters import ReferenceFilterSet

from datasets.models import Reference, Change
from data import get
from data.views import Create, Update

from media.views import store_in_s3

from add.forms import handlePopAdd

bucket = "darticles"


def index(request):
    datasets = get(title='Datasets')
    return render_to_response('datasets/index.html', {'datasets': datasets},
        context_instance=RequestContext(request))


class ReferenceCreate(Create):
    model = Reference
    form_class = ReferenceForm
    comment = "Created reference"
    success_url = '/datasets/references/'


class ReferenceUpdate(Update):
    model = Reference
    form_class = ReferenceForm
    comment = "Updated reference"



class ReferenceList(SingleTableView, FormView):
    template_name = 'datasets/reference_table.html'
    context_object_name = 'references'
    table_class = ReferenceTable
    form_class = FilterForm
    success_url = '/datasets/references/'
    model = Reference
    query = None
    queryset = Reference.objects.all().order_by('-id')

    def form_valid(self, form):
        ReferenceList.query = form.cleaned_data['filter']
        return super(ReferenceList, self).form_valid(form)

    def form_invalid(self, form):
        ReferenceList.query = None
        return super(ReferenceList, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ReferenceList, self).get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={'filter': ReferenceList.query})
        context['entry'] = get(title='References')
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        qs = self.queryset
        query = ReferenceList.query
        if query:
            terms = query.split(None)
            if len(terms) == 1:
                try:
                    qs = qs.filter(pmid=terms[0])
                except Exception as e:
                    qs = qs.filter(Q(title__icontains=terms[0]) |
                                                   Q(authors__icontains=terms[0]) |
                                                   Q(abstract__icontains=terms[0]) |
                                                   Q(keywords__icontains=terms[0]) |
                                                   Q(notes__icontains=terms[0]))
            else:
                for term in terms:
                    qs = qs.filter(Q(title__icontains=term) |
                                                      Q(authors__icontains=term) |
                                                      Q(abstract__icontains=term) |
                                                      Q(keywords__icontains=term) |
                                                      Q(notes__icontains=term))
        self.filterset = ReferenceFilterSet(qs, self.request.GET)
        return self.filterset.qs


def detail(request, pk, template="datasets/reference_detail.html"):
    try:
        object = Reference.objects.get(pk=pk)
    except Reference.DoesNotExist:
        try:
            object = Reference.objects.get(pmid=pk) #, created  get_or_create +/- reversion. return redirect('/datasets/reference/create/')
        except:
            return redirect('https://www.ncbi.nlm.nih.gov/pubmed/%s' % pk)
    if not request.method == "POST":
        form = UploadForm()
    else:
        form = UploadForm(request.POST, request.FILES)
        file = request.FILES['file']
        store_in_s3(file.name, file.read(), bucket)
        object.url = "http://%s.s3.amazonaws.com/%s" % (bucket, file.name)
        object.save()
    ctx = {'form': form, 'object': object}
    return render(request, template, ctx)

def references_archive(request):
    references = Reference.objects.all()
    references_entry = get(title='References')
    ctx = {'references': references, 'references_entry': references_entry}
    return render_to_response('datasets/reference_archive.html', ctx,
        context_instance=RequestContext(request))

def update_references(request):
    Reference.update()
    render_to_response('datasets/index.html',
                      context_instance=RequestContext(request))

#        try:
#        except ValueError:
#            print "Error, by retrieving pubmed data.", i.pmid, len(r), type(r)
#            try:
#                for k, v in r[0].items():
#                    print k,':', v
#            except KeyError: "Print got an KeyError"
#        except: print('Failed retieving information for %s' % i)
#    return HttpResponse('Updated!')

def autoupdate_reference(request, pk):
    reference = Reference.objects.get(pk=pk)
    reference.save(update=True)
    return render_to_response('datasets/reference_detail.html', {'object': reference},
        context_instance=RequestContext(request))


def duplicates(request):
    dups = Reference.duplicates()
    return render_to_response('datasets/reference_archive.html', {'references': dups},
                              context_instance=RequestContext(request))

def changes(request):
    changes = Change.objects.all()
    changes_description = get(title='Biological Changes')
    ctx = {'changes': changes, 'changes_description': changes_description}
    return render(request, 'datasets/changes.html', ctx)



def newReference(request):
    if isinstance(request.user, AnonymousUser):
        request.user = User.objects.get(username="Anonymous")
    return handlePopAdd(request, ReferenceForm, 'reference')
