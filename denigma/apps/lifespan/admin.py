# -*- coding: utf-8 -*-
from django.contrib import admin

import reversion

from mptt.admin import MPTTModelAdmin

from django_tablib.admin import TablibAdmin

from models import Study, Experiment, Measurement, Comparison, Epistasis, Strain
from models import Type, Factor, Manipulation, Intervention, Regimen, Assay, Gender
from models import Variant, StudyType, Population, State, Technology, VariantType, ORType


class StudyAdmin(reversion.VersionAdmin):
    fields = ['title', 'pmid', 'link', 'reference', 'species', 'notes', 'integrated']
    list_display = ('title', 'pmid', 'full_text', 'notes', 'created', 'updated', 'integrated')
    search_fields = ('title', 'pmid', 'notes')

    def full_text(self, obj):
        if obj.link:
           return '<a href="%s">%s</a>' % (obj.link, 'available')
        else:
           return 'not linked'
    full_text.allow_tags = True


class ExperimentAdmin(reversion.VersionAdmin):
    list_display = ('name', 'study')


class MeasurementAdmin(reversion.VersionAdmin):
   list_display = ('genotype', 'mean', 'median', 'max')


class ComparisonAdmin(reversion.VersionAdmin):
   list_display = ('__unicode__', 'mean', 'median', 'max')


class EpistasisAdmin(reversion.VersionAdmin):
    pass


class StrainAdmin(reversion.VersionAdmin):
    search_fields =('name',)


class TypeAdmin(reversion.VersionAdmin):
    list_display = ('name',)


class AdminFactor(reversion.VersionAdmin):
    list_display = ('symbol',
                    'name',      
                    'taxid',
                    'function',
                    'observation',
                    'reference',
                    'human_homologue',
                    )
    list_filter = ['taxid',
                   'classifications',
                   'mapping', 'regimen'] #'manipulation',   #'classification',

    search_fields = ['symbol', 'name', 'observation', 'alias', 'entrez_gene_id', 'ensembl_gene_id',
                     'description', 'function', 'human_homologue', 'pubmed_id', 'reference']#'observation', 
    fieldsets = [
        (None, {'fields': ['symbol', 'name', 'taxid']}),
        ('Annotation', {'fields': ['entrez_gene_id', 'ensembl_gene_id', 'alias'], 'classes': ['collapse']}),
        ('Description', {'fields': ['function', 'observation']}),
        ('Lifespan Impact', {'fields': ['_25', 'mean', 'median', '_75', 'maximum'], 'classes': ['collapse']}),
        (None, {'fields': ['classifications', 'intervention', 'assay', 'regimen', 'references']}),
        ('Others', {'fields': ['description', 'pubmed_id', 'reference', 'life_span', 'classification', 'manipulation', 'gene_intervention', 'synergistic_epistasis', 'antagonistic_epistasis', 'human_homologue', 'type', 'types', 'note'], 'classes': ['collapse']})
    ]        
    filter_horizontal = ['classifications', 'regimen', 'intervention', 'references']


class ManipulationAdmin(reversion.VersionAdmin):
    list_display = ('shortcut', 'name')
    fields = ('shortcut', 'name', 'type')
    filter_horizontal = ('type',)
##    inlines = [ManipulationTypeInline]


class ManipulationTypeInline(admin.StackedInline): #http://charlesleifer.com/blog/self-referencing-many-many-through/
    model = Manipulation
    fk_name = 'type_of'


class InterventionAdmin(reversion.VersionAdmin):
    list_display = ('name', 'effect', 'mean', 'median', '_75', 'maximum','pmid')
    fields = ('name', 'taxid', 'species', 'effect', 'mean', 'median', '_25', '_75', 'maximum','pmid', 'references', 'manipulation')
    search_fields = ['name', 'pmid', 'effect']    
    list_filter = ('taxid', 'species', 'manipulation')
    #raw_id_fields = ('reference',)
    filter_horizontal = ('references','manipulation',)


class RegimenAdmin(reversion.VersionAdmin):
    list_display = ('shortcut', 'name')


class AssayAdmin(reversion.VersionAdmin):
    list_display = ('shortcut', 'name')


# class VariantAdminForm(forms.ModelForm):
#     formfield_overrides = {
#         models.TextField: {'widget': AdminPagedownWidget},
#     }
#     text = forms.CharField(widget=AdminPagedownWidget(
#         attrs={'rows': 30, 'cols': 80, 'style': 'font-family:monospace'}),
#         help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/'
#                   'quickref.html">reStructuredText Quick Reference</a>'
#     )
#     references = forms.ModelMultipleChoiceField(
#         label='Factors',
#         queryset=Factor.objects.all(),
#         required=False,
#         help_text='Lifespan factors.',
#         widget=admin.widgets.FilteredSelectMultiple('references', False)
#     )
#
#
# class EntryAdmin(reversion.VersionAdmin):
#     search_fields = ('title', 'text', 'url')
#     ordering = ('-created',)
#     list_filter = ('published',)
#     #inlines = [ChangeInline]
#     #inlines = [RelationInline]
#
#     form = EntryAdminForm


class VariantAdmin(TablibAdmin, reversion.VersionAdmin):
    list_display = ('polymorphism', 'variant_type', 'factor', 'odds_ratio', 'or_type', 'pvalue', 'p_value', 'significant', 'description', # 'qvalue',
                    'initial_number', 'replication_number', 'age_of_cases', 'technology',
                    'study_type',  'pmid', 'created', 'updated' ) #'reference',
    fields = ('polymorphism', 'alias', 'variant_type', 'location', 'factor', 'factors', 'description', 'finding', 'odds_ratio', 'or_type', 'pvalue', 'p_value', 'qvalue',
              'significant','initial_number', 'replication_number', 'ethnicity', 'age_of_cases', 'study_type',
              'technology', 'pmid', 'reference', 'choice', 'classifications')
    search_fields = ['description', 'alias', 'polymorphism',  'odds_ratio', 'pvalue', 'p_value',  'qvalue', 'significant', #'factor', 'technology', 'study_type',  'reference',
                    'initial_number', 'replication_number', 'age_of_cases',  'finding', #'variant_type', 'or_type',
                     'pmid', 'shorter_lived_allele', 'longer_lived_allele',
                     'odds_ratio', 'pvalue', 'p_value', 'qvalue', 'significant', 'initial_number', 'age_of_cases'] #, 'choice'
    list_filter = ('study_type', 'choice', 'finding', 'variant_type','finding', 'or_type', 'created', 'updated', 'ethnicity', 'classifications',)#'factors',
    filter_horizontal = ('factors', 'ethnicity', 'classifications')
    formats = ['xls', 'json', 'yaml', 'csv', 'html']

class StudyTypeAdmin(reversion.VersionAdmin):
    search_fields = ['name']

class PopulationAdmin(MPTTModelAdmin):
    search_fields = ['name']

class StateAdmin(reversion.VersionAdmin):
    search_fields = ['name']

class TechnologyAdmin(reversion.VersionAdmin):
    search_fields = ['name']

class VariantTypeAdmin(reversion.VersionAdmin):
    search_fields = ['name']

class ORTypeAdmin(reversion.VersionAdmin):
    search_fields = ['name']

admin.site.register(Study, StudyAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Comparison, ComparisonAdmin)
admin.site.register(Epistasis, EpistasisAdmin)
admin.site.register(Strain, StrainAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Factor, AdminFactor)
admin.site.register(Manipulation, ManipulationAdmin)
admin.site.register(Intervention, InterventionAdmin)
admin.site.register(Regimen, RegimenAdmin)
admin.site.register(Assay, AssayAdmin)
admin.site.register(Gender)
admin.site.register(Variant, VariantAdmin)
admin.site.register(StudyType, StudyTypeAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(VariantType, VariantTypeAdmin)
admin.site.register(ORType, ORTypeAdmin)
