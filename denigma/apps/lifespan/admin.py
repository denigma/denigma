from django.contrib import admin

from models import Study, Experiment, Measurement, Comparision, Epistasis, Strain
from models import Type, Factor, Manipulation, Intervention, Regimen, Assay


class StudyAdmin(admin.ModelAdmin):
    fields = ['title', 'pmid', 'reference', 'notes', 'integrated']
    list_display = ('title', 'pmid', 'notes', 'created', 'updated', 'integrated')


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name', 'study')


class MeasurementAdmin(admin.ModelAdmin):
   list_display = ('genotype', 'mean', 'median', 'max')


class ComparisionAdmin(admin.ModelAdmin):
   list_display = ('__unicode__', 'mean', 'median', 'max')


admin.site.register(Study, StudyAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Comparision, ComparisionAdmin)
admin.site.register(Epistasis)
admin.site.register(Strain)

class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Type, TypeAdmin)


class AdminFactor(admin.ModelAdmin):
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
                   'mapping'] #'manipulation',   #'classification',

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

admin.site.register(Factor, AdminFactor)


class ManipulationAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'name')
    fields = ('shortcut', 'name', 'type')
    filter_horizontal = ('type',)
##    inlines = [ManipulationTypeInline]
admin.site.register(Manipulation, ManipulationAdmin)

class ManipulationTypeInline(admin.StackedInline): #http://charlesleifer.com/blog/self-referencing-many-many-through/
    model = Manipulation
    fk_name = 'type_of'

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('name', 'effect', 'mean', 'median', '_75', 'maximum','pmid')
    fields = ('name', 'taxid', 'effect', 'mean', 'median', '_25', '_75', 'maximum','pmid', 'references', 'manipulation')
    search_fields = ['name', 'pmid', 'effect']    
    list_filter = ('taxid', 'manipulation')
    #raw_id_fields = ('reference',)
    filter_horizontal = ('references','manipulation',)
admin.site.register(Intervention, InterventionAdmin)


class RegimenAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'name')
admin.site.register(Regimen, RegimenAdmin)


class AssayAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'name')
admin.site.register(Assay, AssayAdmin)


##class SpeciesAdmin(admin.ModelAdmin):
##    list_dispaly = ('taxid',)
##admin.site.register(Species, SpeciesAdmin)
