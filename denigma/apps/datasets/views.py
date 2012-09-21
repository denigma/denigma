# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from datasets.models import Reference, Change
from blog.models import Post


def index(request):
    datasets = Post.objects.get(title='Datasets')
    return render_to_response('datasets/index.html', {'datasets': datasets},
                              context_instance=RequestContext(request))

def references(request):
    references = Reference.objects.all()
    references_entry = Post.objects.get(title='References')
    ctx = {'references': references, 'references_entry': references_entry}
    return render_to_response('datasets/references.html', ctx,
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

def duplicates(request):
    dups = Reference.duplicates()
    return render_to_response('datasets/references.html', {'references': dups},
                              context_instance=RequestContext(request))

def changes(request):
    changes = Change.objects.all()
    changes_description = Post.objects.get(title='Changes')
    ctx = {'changes': changes, 'changes_description': changes_description}
    return render(request, 'datasets/changes.html', ctx)