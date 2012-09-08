# -*- coding: utf-8 -*-
import datetime

from datasets.models import Reference, Change
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.template import RequestContext


def index(request):
    return render_to_response('datasets/index.html', context_instance=RequestContext(request))

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

def duplicates(request):
    dups = Reference.duplicates()
    return render_to_response('datasets/references.html', {'references': dups},
                              context_instance=RequestContext(request))

def references(request):
    references = Reference.objects.all()
    return render_to_response('datasets/references.html', {'references': references},
                              context_instance=RequestContext(request))

