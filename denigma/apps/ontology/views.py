import os
from random import random
from textwrap import wrap

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import simplejson

from models import Entity, Relation

from blog.templatetags.hyperlink import hyper
from blog.templatetags.crosslink import recross
from data.templatetags.rendering import markdown


color_key = {'blue': 'Nucleus & Endoplasmic Reticulum',
             'tan narrow': 'Cytoplasmic molecules',
             'light_blue': 'Mitochondria',
             'brown': 'Extracellular Proteins, etc.',
             'pink': 'Controlled Degradation',
             'green': 'Beneficial process or intervention',
             'purple': 'Signaling Pathway',
             'red': 'Damaging Substance or Process',
             'black': 'Senescence Physiology'}

shape_key = {
    'narrow': 'Causal Sequence of Events',
    'width': 'Movement'
}

def index(request, template='ontology/index.html'):
    #print("index")
    ctx = {'entities': Entity.objects.all(),
           'relations': Relation.objects.all()}
    return render(request, template, ctx)

def delete(request, template='ontology/index.html'):
    Entity.objects.all().delete()
    return redirect('ontology')

def load(request, template='ontology/load.html'):
    Entity.objects.all().delete()

    path = os.path.join(settings.PROJECT_ROOT, 'apps', 'ontology', 'nodes.csv')
    nodes = file(path).read().split('\n')[1:]
    for node in nodes:
        if not node: continue
        columns = node.split('\t')

        if len(columns) <= 5: columns.append('')
        print len(columns), columns
        shape_number, shape_key, text, shape_color, region_color1, region_color2 = columns
        Entity.objects.create(pk=int(shape_number),title=text.replace('"', ''), text='\n'.join([shape_key, shape_color, region_color1, region_color2]))

    path = os.path.join(settings.PROJECT_ROOT, 'apps', 'ontology', 'connections.csv')
    links = file(path).read().split('\n')[2:]
    for link in links:
        if not link: continue
        from_node, arrow_color, width, to_node, x_at_end = link.split('\t')
        if to_node == '-': continue
        entity, created = Entity.objects.get_or_create(title=arrow_color, text="\n".join([width, x_at_end]))
        print link.split('\t')
        Relation.objects.create(source=Entity.objects.get(pk=int(from_node)), type=entity, target=Entity.objects.get(pk=int(to_node)))

    #ctx = {'entities':Entity.objects}

    return redirect('ontology')

def graph(request, template='ontology/graph.html'):
    """View that generates a data graph connecting data entries with relations."""
    network = {
        'dataSchema': {
            'nodes': [
                {'name': 'label', 'type': 'string'},
                {'name': 'text', 'type': 'string'},
                {'name': 'links', 'type': 'string'},
                {'name': 'weight', 'type': 'number'},
                {'name': 'shape', 'type': 'string'},
                {'name': 'color', 'type': 'string'}

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

    def wrapping(text, at=10):
        return "\n".join(wrap(text, width=at))

    def node(entry):
        "Helper function to construct a node object."
        memo.append(entry.pk)
        attributes = entry.text.split('\n')
        return {'id': str(entry.pk), 'label': wrapping(entry.title), 'text': entry.text, #recross(hyper(markdown()))
                'links': '<a href="%s">View</a>' %
                         (entry.get_absolute_url()), 'weight':random(),
                'shape': attributes[0],
                'color': attributes[1]
        }

    # Getting the actually data:
    data = {'nodes':[], 'edges':[]}
    relations = Relation.objects.all()
    for relation in relations:
        fr = relation.source
        be = relation.type
        to = relation.target
        if fr.pk not in memo:
            data['nodes'].append(node(fr))
        if to.pk not in memo:
            data['nodes'].append(node(to))

        data['edges'].append({'id': "%sto%s" % (fr.pk, to.pk), 'label': be.title, 'text': be.text, #markdown(),
                              'source': str(fr.pk), 'target': str(to.pk), 'directed': True,
                              'links': '<a href="%s">View</a>' %
                                       (relation.get_absolute_url()), 'weight':random(),
                             }
        )
    network['data'] = data

    network_json = simplejson.dumps(network)
    return render(request, template, {'network_json': network_json})