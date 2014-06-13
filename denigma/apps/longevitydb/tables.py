# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

import django_tables2 as tables

from lifespan.templatetags.pubmed_linker import pubmed_links

from lifespan.models import Variant


class VariantTable(tables.Table):

    def render_polymorphism(self, value, record):
         return mark_safe('''<a href=/longevitydb/detail/%s>%s</a>''' % (record.id, value))

    def render_factor(self, value, record):
         return mark_safe('''<a href=/lifespan/factor/%s>%s</a>''' % (record.factor.id, value))

    def render_description(self, value, record):
        return pubmed_links(value)

    def render_ethnicity(self, value, record):
         return mark_safe(", ".join(["<a href='%s'>%s</a>" % (i.get_absolute_url(), i.name) for i in value.all()]))

    def render_reference(self, value, record):
         return mark_safe('''<a href="/datasets/reference/%s>%s"</a>''' % (record.pmid, value.pmid))

    def render_study_type(self, value, record):
        return mark_safe('''<a href="%s">%s</a>''' % (value.get_absolute_url(), value.name))

    # def render_technology(self, value, record):
    #     return mark_safe('''<a href="%s">%s</a>''' % (value.get_absolute_url(), value.name))

    def render_reference(self, value, record):
        return mark_safe('''<a href="%s">%s</a>''' % (value.get_absolute_url(), value.pmid))

    def render_odds_ratio(self, value, record):
        return "%.2f" % round(value, 2)

    class Meta:
        model = Variant
        attrs = {"class": "paleblue"}
        fields = ('polymorphism',  'factor', 'odds_ratio', 'pvalue', #'location',
                  'initial_number', 'replication_number', 'ethnicity',
                  'age_of_cases',  'shorter_lived_allele', 'longer_lived_allele', 'study_type', # 'technology',
                  'reference') # , 'choice'
#        exclude = ('id', 'mapping', 'entrez_gene_id', 'ensembl_gene_id',
#                   'alias', 'description', 'functional_description',
#            'classification', 'manipulation,' 'observation',
#            'mean','median', 'max', '_25', '_75')
