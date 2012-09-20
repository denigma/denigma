"""Annotation views."""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post

from models import Classification, Tissue, Species, Taxonomy


def index(request):
    annotations = Post.objects.get(title='Annotations') 
    return render_to_response('annotations/index.html',
                              {'annotations': annotations},
                               context_instance=RequestContext(request))

def classifications(request):
    classifications = Classification.objects.all()
    return render_to_response('annotations/classifications.html',
                              {'classifications': classifications},
                              context_instance=RequestContext(request))

def classification(request, pk):
    classification = Classification.objects.get(pk=pk)
    return render_to_response('annotations/classification.html',
                              {'classification': classification},
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
        page = pageinator.page(paginator.num_pages)
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
    pass

def tissues(request):
    """Lists all the tissues with pagination (Pagination is not yet implemented)."""
    tissues = Tissue.objects.all()
    return render_to_response('annotations/tissues.html', {'tissues': tissues},
                              context_instance=RequestContext(request))

def tissue(request, pk):
    """Gives a the details of a specific tissue/cell type."""
    tissue = Tissue.objects.get(pk=pk)
    return render_to_response('annotations/tissue.html', {'tissue': tissue},
                              context_instance=RequestContext(request))

def tissue_archive(request):
    """Generates a simple archive list of all the tissues
    (with and without pagination on click)."""
    tissues = Tissue.objects.all()
    ctx = {'tissues': tissues}
    return render_to_response('annotations/tissue_archive.html', ctx,
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

#234567891123456789212345678931234567894123456789512345678961234567897123456789
