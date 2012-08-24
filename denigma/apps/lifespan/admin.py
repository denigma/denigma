from django.contrib import admin

#from models import Study, Experiment, Measurement, Comparision, Epistasis
from models import Type, Factor, Manipulation, Intervention, Regimen, Assay


#class StudyAdmin(admin.ModelAdmin):
#    fields = ['title', 'pmid', 'reference', 'notes', 'integrated']
#    list_display = ('title', 'pmid', 'notes', 'created', 'updated', 'integrated')


#class ExperimentAdmin(admin.ModelAdmin):
#    list_display = ('name', 'study')


#class MeasurementAdmin(admin.ModelAdmin):
#   list_display = ('genotype', 'mean', 'median', 'max')


#class ComparisionAdmin(admin.ModelAdmin):
#   list_display = ('__unicode__', 'mean', 'median', 'max')


#admin.site.register(Study, StudyAdmin)
#admin.site.register(Experiment, ExperimentAdmin)
#admin.site.register(Measurement, MeasurementAdmin)
#admin.site.register(Comparision, ComparisionAdmin)
#admin.site.register(Epistasis)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Type, TypeAdmin)


class AdminFactor(admin.ModelAdmin):
    #Change fields to show =
    list_display = ('symbol',
                    #'alias',
                    'name',      
                    'taxid',
                    #'description',
                    'function',
                    'observation',
                    #'pubmed_id',
                    'reference',
                    #s'classification',
                    #'manipulation',
                    #'synergistic_epistasis',
                    #'antagonistic_epistasis',
                    'human_homologue',
                    #'ensembl_gene_id',
                    #'entrez_gene_id',
                    #'mapping',
                    )
    list_filter = ['taxid',
                   'classifications',
                   'mapping'] #'manipulation',   #'classification',

    search_fields = ['symbol', 'name', 'observation', 'alias', 'entrez_gene_id', 'ensembl_gene_id',
                     'description', 'function', 'human_homologue', 'pubmed_id', 'reference']#'observation', 
##    fields = ('entrez_gene_id', 'ensembl_gene_id', 'symbol', 'name', 'alias', 'taxid',
##              'function', 'observation', 'classification', 'classifications', 'lifespan', 'intervention',
##              'pubmed_id', 'references', 'references',
##              'mean', 'median', '_25', '_75', 'maximum', 'manipulation')#'pmids'

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
