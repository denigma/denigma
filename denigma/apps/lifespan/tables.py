# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

import django_tables2 as tables

from templatetags.pubmed_linker import pubmed_links

from models import Intervention, Factor, Comparison, Variant


class InterventionTable(tables.Table):

    def render_name(self, value, record):
        return mark_safe('''<a href=/lifespan/intervention/%s>%s</a>''' % (record.id, value))

    def render_species(self, value, record):
        return mark_safe('''<a href=/annotations/species/%s>%s</a>''' % (value.pk, value.short_name))

    def render_effect(self, value, record):
        return pubmed_links(value)

    class Meta:
        model = Intervention
        # add class ="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        exclude = ('id', 'taxid', 'strain',  '_25', '_75', 'sex', 'background', 'lifespans', 'pmid')


class FactorTable(tables.Table):

    def render_symbol(self, value, record):
        return mark_safe('''<a href=/lifespan/factor/%s>%s</a>''' % (record.id, value))

    def render_name(self, value, record):
        if not record.symbol:
            return mark_safe('''<a href=/lifespan/factor/%s>%s</a>''' % (record.id, value))
        return value

    def render_observation(self, value, record):
        return pubmed_links(value)

    def render_species(self, value, record):
        return mark_safe('''<a href=/annotations/species/%s>%s</a>''' % (value.taxid, value))

    class Meta:
        model = Factor
        attrs = {"class": "paleblue"}
        fields = ('symbol', 'name', 'observation', 'species')
#        exclude = ('id', 'mapping', 'entrez_gene_id', 'ensembl_gene_id',
#                   'alias', 'description', 'functional_description',
#            'classification', 'manipulation,' 'observation',
#            'mean','median', 'max', '_25', '_75')

class VariantTable(tables.Table):

    def render_polymorphism(self, value, record):
         return mark_safe('''<a href=/lifespan/variant/%s>%s</a>''' % (record.id, value))

    def render_factor(self, value, record):
         return mark_safe('''<a href=/lifespan/factor/%s>%s</a>''' % (record.factor.id, value))

    def render_description(self, value, record):
        return pubmed_links(value)

    def render_ethnicity(self, value, record):
         return mark_safe(", ".join([i.name for i in value.all()]))

    def render_reference(self, value, record):
         return mark_safe('''<a href=/datasets/reference/%s>%s</a>''' % (record.pmid, value.pmid))

    class Meta:
        model = Variant
        attrs = {"class": "paleblue"}
        fields = ('polymorphism',  'factor', 'odds_ratio', 'pvalue', #'location',
                  'initial_number', 'replication_number', 'ethnicity',
                  'age_of_cases',  'shorter_lived_allele', 'longer_lived_allele', 'study_type', 'technology',
                  'reference') # , 'choice'
#        exclude = ('id', 'mapping', 'entrez_gene_id', 'ensembl_gene_id',
#                   'alias', 'description', 'functional_description',
#            'classification', 'manipulation,' 'observation',
#            'mean','median', 'max', '_25', '_75')


class ComparisonTable(tables.Table):

    def render_id(self, value, record):
        return mark_safe('''<a href=/lifespan/comparison/%s/>%s</a>''' % (value, value)) #record.__unicode__()

    def render_exp(self, value, record):
        return mark_safe('''<a href=/lifespan/measurement/%s/>%s</a>''' % (value.id, value))

    def render_ctr(self, value, record):
        return mark_safe('''<a href=/lifespan/measurement/%s/>%s</a>''' % (value.id, value))

    def render_intervention(self, value, record):
        return mark_safe('''<a href=/lifespan/intervention/%s/>%s</a>''' % (value.id, value))

    def render_manipulation(self, value, record):
        manipulation = record.exp.manipulation
        if manipulation:
            return mark_safe('''<a href=/lifespan/manipulation/%s/>%s</a>''' % (record.exp.manipulation.pk, record.exp.manipulation.shortcut))
        else:
            return "-"



    class Meta:
        model = Comparison
        attrs = {"class": "paleblue"}
        fields = ('id', 'exp', 'ctr', 'manipulation', 'intervention', 'mean', 'median', 'max', 'pvalue', 't', 'gender', 'epistasis') #'exp_t', 'ctr_t')


#234567891123456789212345678931234567894123456789512345678961234567897123456789