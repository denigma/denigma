# -*- coding: utf-8 -*-
import os
import fileinput

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.db import connection
from django.db.models import Q

from data import get
from data.filters import TableFilter
from utils import is_int

from models import Interaction
from tables import InteractionTable
from filters import InteractionFilterSet
from integrator import main


def index(request, template='interactions/index.html'):
    entry = get("Interactions")
    return render(request, template, {'entry': entry})


class InteractionList(TableFilter):
    model = Interaction
    table_class = InteractionTable
    queryset = Interaction.objects.all()
    success_url = '/interactions/table/'

    def get_queryset(self):
        qs = self.queryset
        if InteractionList.query:
            terms = InteractionList.query.split(None)
            for term in terms:
                if is_int(term):
                    qs = qs.filter(Q(id_a=term) | Q(id_b=term))
                else:
                    qs = qs.filter(Q(alias_a__icontains=term) |
                                   Q(alias_b__icontains=term))
        self.filterset = InteractionFilterSet(qs, self.request.GET)
        return self.filterset.qs


class InteractionRDF(ListView):
    """Generates RDF data from interactions."""
    model = Interaction
    queryset = Interaction.objects.all()[:1000]
    template_name = 'interactions/rdf.html'

    def get_context_data(self, **kwargs):
        context = super(InteractionRDF, self).get_context_data(**kwargs)
        interactions = self.queryset.all()

        result = ['@prefix <http://xmlns.com/foaf/0.1/>\n',
                 '@de: <http://denigma.de/data/entry/>\n']
        for interaction in interactions:
            #print(interaction)
            result.append('<http://www.ncbi.nlm.nih.gov/gene/%s> foaf:alias ,' % interaction.id_a)
            result.append(interaction.alias_a.replace('; ', ','))
            if interaction.alias_a:
                for alias in interaction.alias_a.split('; ')[1:]:
                    result.append('%s' % alias)

            result.append('.\n<http://www.ncbi.nlm.nih.gov/gene/%s> foaf:alias ,' % interaction.id_b)
            result.append(interaction.alias_b.replace('; ', ','))
            if interaction.alias_b:
                for alias in interaction.alias_b.split('; ')[1:]:
                    result.append('%s' % alias)

            result.append('.\n<http://www.ncbi.nlm.nih.gov/gene/%s> de:interactsWith <http://www.ncbi.nlm.nih.gov/gene/%s> .' % (interaction.id_a, interaction.id_b))

            #result.extend(['<http://www.ncbi.nlm.nih.gov/gene/%s> foaf:alias ,' % interaction.id_a,
            #interaction.alias_a.replace('; ', ', '),
           # '.\n<http://www.ncbi.nlm.nih.gov/gene/%s> foaf:alias ,' % interaction.id_b,
           # '.\n<http://www.ncbi.nlm.nih.gov/gene/%s> de:interactsWith <http://www.ncbi.nlm.nih.gov/gene/%s> .' % (interaction.id_a, interaction.id_b)])
        context['interactions'] = "".join(result)
        return context

def update(request, db="BioGRID"):
    exec("from %s import main" % db)
    main()
    return redirect('/interactions/')

def integrator(request, memory=True, header=False):

    main(memory=memory, header=header)
    pathToFile = os.path.join(settings.PROJECT_ROOT, 'apps', 'interactions', 'merged.txt')
    fields = ('id_a', 'id_b',
              'alias_a', 'alias_b',
              'system', 'type', 'method', 'modification',
              'taxid_a', 'taxid_b',
              'pmid', 'source', 'score')

    # Raw sql triggered direct insertion of the file:
    sql = "load data infile '%s' into table %s_%s columns terminated by '\t'"\
     "lines terminated by '\n'(%s);"\
          % (pathToFile,'interactions','interaction'"", ", ".join(fields))


#234567891123456789212345678931234567894123456789512345678961234567897123456789

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE interactions_interaction;')
    cursor.execute(sql)
    #row = cursor.fetchone()
    #print row

    print sql
    query = Interaction.objects.raw(sql)
    #    print query


    # Reading and inserting via Django ORM (works, but is too slow):
#    f = fileinput.input(os.path.join(settings.PROJECT_ROOT, 'apps', 'interactions', 'merged.txt'))
#    interactions = []
#    for line in f:
#        if header:
#            header = False
#            continue
#        values = line.replace('\n', '').split('\t')
#        #print values
#        input = dict(zip(fields, values))
#        interaction = Interaction()
#        interaction.__dict__.update(input)
#        #interaction.save()
#        interactions.append(interaction)
#    f.close()
#    Interaction.objects.bulk_create(interactions)





     # Alternative direct insertion via python-MySQLdb:
#    import MySQLdb as mysql
#    mydb = mysql.connect(user='root', db='denigma')
#    cursor = mydb.cursor()
#    handle = cursor.execute(sql)
#    print handle

    msg = "Successfully integrated interactions"
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('/interactions/')


#234567891123456789212345678931234567893