from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse

from blog.models import Post
from models import Tissue


def index(request):
    annotations = Post.objects.get(title='Annotations') 
    return render_to_response('annotations/index.html', {'annotations': annotations},
                              context_instance=RequestContext(request))

#def bulk_upload(request):
#   return render_to_response('annotations/bulk_upload.html',
#                             context_instance=RequestContext(request))

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
    msg = "Received %s lines of data on %s for model %s" % (len(data)-1, header.values(), model_name)
    messages.add_message(request, messages.SUCCESS, ugettext(msg))
    return HttpResponseRedirect('/annotations/')


def species(request):
    return render_to_response('annotations/species.html',
                              context_instance=RequestContext(request))         

def tissues(request):
    tissues = Tissue.objects.all()
    return render_to_response('annotations/tissues.html', {'tissues': tissues},
                              context_instance=RequestContext(request))

def tissue(request, pk):
    tissue = Tissue.objects.get(pk=pk)
    return render_to_response('annotations/tissue.html', {'tissue': tissue},
                              context_instance=RequestContext(request))
