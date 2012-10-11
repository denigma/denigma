from django.contrib import admin

import reversion
#from mptt.admin import MPTTModelAdmin

from models import *


class TissueAdmin(reversion.VersionAdmin):
    list_display = ('name', 'description', 'synonyms')
    search_fields = ['name', 'description', 'synonyms', 'notes']


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('taxid', 'scientific_name')
    search_fields = ['taxid', 'scientific_name']


class AnimalAdmin(reversion.VersionAdmin):
    list_display = ('taxid',
                    'alternative_names')
    search_fields = ['taxid',
                    'alternative_names', 'common_names', 'genbank_synonym']


class SpeciesAdmin(reversion.VersionAdmin):
    list_display = ('taxid',
                    'short_name',
                    'common_name',
                    'latin_name',
                    'short_latin_name',
                    'number_genes',
                    'gendr_genes',
                    'gendr_orthologs',
                    'gendr_paralogs')#,'alternative_names
##    #list_filter = []
##    search_fields = ['taxid',
##                    'short_name',
##                    'common_name',
####                    'alternative_names_id',
##                    'latin_name',
##                    'latin_shortcut']


class ClassificationAdmin(reversion.VersionAdmin): # MPTTModelAdmin
    list_display = ('title', 'abbreviation', 'slug', 'description')
    search_fields = ['title', 'abbreviation', 'slug', 'description']


class GeneAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol','entrez_gene_id', 'taxid', 'classes', 'NCBI', 'wiki', 'SGD')
    list_filter = ['taxid', 'classes']
    search_fields = ['gene_symbol', 'entrez_gene_id']
    def wiki(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    wiki.allow_tags = True     #allow tags to a string
    
    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string
    
    def SGD(self,obj):
        return u"<a href='http://www.yeastgenome.org/cgi-bin/locus.fpl?locus=%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    SGD.allow_tags = True    #allow tags to a string


class DiscontinuedIdAdmin(admin.ModelAdmin):
    fields = ['discontinued_id', 'entrez_gene_id']
    list_display = ('discontinued_id', 'entrez_gene_id')


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id',
                    'gene_symbol',
                    'gene_name',
                    's',
                    't',
                    'specificity',
                    'p_value',
                    'classification',
                    'query',
                    'seed',
                    'taxid',
                    'dr',
                    'NCBI',
                    'wiki',
                    'SGD',
                    'yeast_homolog_symbol',
                    'worm_homolog_symbol',
                    'fly_homolog_symbol',
                    'mouse_homolog_symbol',
                    'human_homolog_symbol')
    list_filter = ['taxid', 'seed', 'query',]
    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']

    def wiki(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    wiki.allow_tags = True     #allow tags to a string
    
    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string
    
    def SGD(self,obj):
        return u"<a href='http://www.yeastgenome.org/cgi-bin/locus.fpl?locus=%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    SGD.allow_tags = True    #allow tags to a string

    #allow editing of filed
    #list_editable = ('gene_name',)


class EntrezAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'gene_symbol', 'gene_name', 'locus_tag', 'symbol_from_nomeclature_authority', 'full_name_from_nomenclature_autority', 'ensembl_gene_id', 'mirbase', 'mgi', 'hgnc', 'mim', 'hprd', 'rgd', 'ratmap', 'wormbase_id', 'imgt_gene_db', 'taxid')
    search_fields = ['gene_symbol', 'locus_tag','ensembl_gene_id']
    list_filter = ['taxid']


class GOAdmin(admin.ModelAdmin):
    list_display = ('taxid', 'entrez_gene_id', 'go_id', 'evidence', 'qualifier', 'go_term', 'pmid', 'category', 'NCBI', 'Article')
    search_fields = ['entrez_gene_id', 'go_id', 'go_term', 'pmid']
    list_filter = ['taxid','evidence', 'category', 'qualifier']
    
    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string

    def Article(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/pubmed/%s'>link</a>" % obj.pmid
    Article.allow_tags = True     #allow tags to a string   


class SGD_featuresAdmin(admin.ModelAdmin):
    list_display = ('sgd_id', 'feature_type', 'feature_qualifier', 'ensembl_gene_id', 'gene_symbol', 'alias', 'parent_feature_name', 'secondary_sgd_id', 'chromosome', 'start_coordinate', 'stop_coordinate', 'strand', 'genetic_position', 'coordinate_version', 'sequence_version', 'description')
    search_fields = [ 'ensembl_gene_id', 'gene_symbol', 'alias', 'description']


class SGD_gene_associationAdmin(admin.ModelAdmin):
    list_display = ('sgd_id', 'gene_symbol', 'with_or_from', 'go_id', 'reference', 'evidence', 'other_ids', 'category', 'gene_name', 'orf', 'date', 'source')


class HomoloGeneAdmin(admin.ModelAdmin):
    list_display = ('hid', 'taxid', 'entrez_gene_id', 'gene_symbol', 'protein_gi', 'protein_accession')
    search_fields = ['hid', 'entrez_gene_id', 'gene_symbol', 'protein_gi', 'protein_accession']
    list_filter = ['taxid']


class InParanoidAdmin(admin.ModelAdmin):
    list_display = ('group_number', 'ensembl_gene_id_a', 'ensembl_gene_id_b', 'taxid_a', 'taxid_b')
    search_fields = ['ensembl_gene_id_a', 'ensembl_gene_id_b']


class gene2ensemblAdmin(admin.ModelAdmin):
    list_display = ('taxid', 'entrez_gene_id', 'ensembl_gene_id', 'rna_nucleotide_accession', 'ensembl_rna_id', 'protein_accession', 'ensembl_protein_id')
    search_fields = ['entrez_gene_id', 'ensembl_gene_id']
    list_filter = ['taxid']


class EnsemblEntrezGeneIdAdmin(admin.ModelAdmin):
    list_display = ('ensembl_gene_id', 'entrez_gene_id', 'taxid')
    search_fields = ['entrez_gene_id', 'ensembl_gene_id']
    list_filter = ['taxid']


class GenAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id',
                    'gene_symbol',
                    'gene_name',
                    'taxid',
                    'classification',
                    'NCBI',
                    'wiki',
                    'SGD')
    
    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string
    
    def wiki(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    wiki.allow_tags = True     #allow tags to a string
    
    def SGD(self,obj):
        return u"<a href='http://www.yeastgenome.org/cgi-bin/locus.fpl?locus=%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    SGD.allow_tags = True    #allow tags to a string

    list_filter = ['taxid',
    'ageing_associated',
    'ageing_methylated',
    'positive_gerontogene',
    'negative_gerontogene',
    'positive_ageing_suppressor',
    'negative_ageing_suppressor',
    'longevity_associated',
    'ageing_differential',
    'ageing_induced',
    'ageing_suppressed',
    'dr_essential',
    'dr_essential_ortholog',
    'dr_differential',
    'dr_induced',
    'dr_suppressed',
    'core_clock',
    'clock_modulator',
    'clock_modulator_ortholog',
    'circadian_differential',
    'clock_systemic',
    'juvenile_differential',
    'juvenile_induced',
    'juvenile_suppressed',
    'embryonic_lethal',
    'senescence_differential',
    'senescence_induced',
    'senescence_suppressed',
    'gerontogene',
    'ageing_suppressor',
    'transcription_factor',
    'pacemaker',
                   'high_amplitude',
                   'long_period',
                   'short_period',
                   'imprinted',
            
    'classification']
    search_fields = ['entrez_gene_id',
                    'gene_symbol',
                    'gene_name',
                    'taxid',
                    'classification'] #'classification', 'reference'


class OrthologAdmin(admin.ModelAdmin):
    list_display = ('ortholog', 'ortholog_symbol', 'ortholog_taxid', 'gene', 'gene_symbol', 'gene_taxid')
    search_fields = ['ortholog', 'ortholog_symbol', 'ortholog_taxid', 'gene', 'gene_symbol']
    list_filter = ['ortholog_taxid', 'gene_taxid']


class Entrez_GeneAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'gene_symbol', 'gene_name', 'locus_tag', 'symbol_from_nomenclature_authority', 'full_name_from_nomenclature_autority', 'ensembl_gene_id', 'mirbase', 'mgi', 'hgnc', 'mim', 'hprd', 'rgd', 'ratmap', 'wormbase_id', 'imgt_gene_db', 'taxid')


admin.site.register(Entrez_Gene, Entrez_GeneAdmin)
admin.site.register(Tissue, TissueAdmin)
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(DiscontinuedId, DiscontinuedIdAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Entrez, EntrezAdmin)
admin.site.register(GO, GOAdmin)
admin.site.register(SGD_features, SGD_featuresAdmin)
admin.site.register(SGD_gene_association, SGD_gene_associationAdmin)
admin.site.register(HomoloGene, HomoloGeneAdmin)
admin.site.register(InParanoid, InParanoidAdmin)
admin.site.register(gene2ensembl, gene2ensemblAdmin)
admin.site.register(EnsemblEntrezGeneId, EnsemblEntrezGeneIdAdmin)
admin.site.register(Gen, GenAdmin)
admin.site.register(Ortholog, OrthologAdmin) 

