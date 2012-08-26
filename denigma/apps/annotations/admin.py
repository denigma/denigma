from annotations.models import * #Classification, Gene, DiscontinuedId, Candidate, Entrez, GO, SGD_features, SGD_gene_association, HomoloGene, EnsemblHomolog,  Orthologs_4932_10090, Orthologs_4932_10116, Orthologs_4932_6239, Orthologs_4932_7227, Orthologs_4932_9544, Orthologs_4932_9606, Paralogs_4932_4932, Orthologs_4932_10090, Orthologs_4932_10116, Orthologs_4932_6239, PotentialOrthologs_4932_9606, PotentialOrthologs_4932_9544, PotentialOrthologs_4932_7227, PotentialOrthologs_4932_6239, PotentialOrthologs_4932_10090,PotentialOrthologs_4932_10116
from django.contrib import admin

class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('taxid', 'scientific_name')
    search_fields = ['taxid', 'scientific_name']
admin.site.register(Taxonomy, TaxonomyAdmin)

class AdminAnimal(admin.ModelAdmin):
    list_display = ('taxid',
                    'alternative_names')
    #list_filter = []
    search_fields = ['taxid',
                    'alternative_names', 'common_names', 'genbank_synonym']
admin.site.register(Animal, AdminAnimal)

class AdminSpecies(admin.ModelAdmin):
    pass
    list_display = ('taxid',
                    'short_name',
                    'common_name',
                    'latin_name',
                    'latin_shortcut',
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
admin.site.register(Species, AdminSpecies)

class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'shortcut')
admin.site.register(Classification, ClassificationAdmin)

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

admin.site.register(Gene, GeneAdmin)

class DiscontinuedIdAdmin(admin.ModelAdmin):
    fields = ['discontinued_id', 'entrez_gene_id']
    list_display = ('discontinued_id', 'entrez_gene_id')
admin.site.register(DiscontinuedId, DiscontinuedIdAdmin)

class AdminCandidate(admin.ModelAdmin):
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
##                    'yeast_homolog_id',
##                    'worm_homolog_id',
##                    'fly_homolog_id',
##                    'mouse_homolog_id',
##                    'human_homolog_id')
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
admin.site.register(Candidate, AdminCandidate)

class AdminEntrez(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'gene_symbol', 'gene_name', 'locus_tag', 'symbol_from_nomeclature_authority', 'full_name_from_nomenclature_autority', 'ensembl_gene_id', 'mirbase', 'mgi', 'hgnc', 'mim', 'hprd', 'rgd', 'ratmap', 'wormbase_id', 'imgt_gene_db', 'taxid')
    search_fields = ['gene_symbol', 'locus_tag','ensembl_gene_id']
    list_filter = ['taxid']
admin.site.register(Entrez, AdminEntrez)

class AdminGO(admin.ModelAdmin):
    list_display = ('taxid', 'entrez_gene_id', 'go_id', 'evidence', 'qualifier', 'go_term', 'pmid', 'category', 'NCBI', 'Article')
    search_fields = ['entrez_gene_id', 'go_id', 'go_term', 'pmid']
    list_filter = ['taxid','evidence', 'category', 'qualifier']
    
    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string

    def Article(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/pubmed/%s'>link</a>" % obj.pmid
    Article.allow_tags = True     #allow tags to a string   
admin.site.register(GO, AdminGO)

class AdminSGD_features(admin.ModelAdmin):
    list_display = ('sgd_id', 'feature_type', 'feature_qualifier', 'ensembl_gene_id', 'gene_symbol', 'alias', 'parent_feature_name', 'secondary_sgd_id', 'chromosome', 'start_coordinate', 'stop_coordinate', 'strand', 'genetic_position', 'coordinate_version', 'sequence_version', 'description')
    search_fields = [ 'ensembl_gene_id', 'gene_symbol', 'alias', 'description']
admin.site.register(SGD_features, AdminSGD_features)

class AdminSGD_gene_association(admin.ModelAdmin):
    list_display = ('sgd_id', 'gene_symbol', 'with_or_from', 'go_id', 'reference', 'evidence', 'other_ids', 'category', 'gene_name', 'orf', 'date', 'source')
admin.site.register(SGD_gene_association, AdminSGD_gene_association)

class HomoloGeneAdmin(admin.ModelAdmin):
    list_display = ('hid', 'taxid', 'entrez_gene_id', 'gene_symbol', 'protein_gi', 'protein_accession')
    search_fields = ['hid', 'entrez_gene_id', 'gene_symbol', 'protein_gi', 'protein_accession']
    list_filter = ['taxid']
admin.site.register(HomoloGene, HomoloGeneAdmin)

##class EnsemblHomologAdmin(admin.ModelAdmin):
##    list_display = ('ensembl_gene_id_a', 'ensembl_gene_id_b', 'homology_type', 'ds', 'dn', 'percentage_identity_a', 'percentage_identity_b', 'taxid_a', 'taxid_b', 'potential_homolog')
##    search_fields = ['ensembl_gene_id_a', 'ensembl_gene_id_b']
##    list_filter = ['taxid_a', 'taxid_a',  'homology_type']
##admin.site.register(EnsemblHomolog, EnsemblHomologAdmin)


class InParanoidAdmin(admin.ModelAdmin):
    list_display = ('group_number', 'ensembl_gene_id_a', 'ensembl_gene_id_b', 'taxid_a', 'taxid_b')
    search_fields = ['ensembl_gene_id_a', 'ensembl_gene_id_b']
admin.site.register(InParanoid, InParanoidAdmin)

class gene2ensemblAdmin(admin.ModelAdmin):
    list_display = ('taxid', 'entrez_gene_id', 'ensembl_gene_id', 'rna_nucleotide_accession', 'ensembl_rna_id', 'protein_accession', 'ensembl_protein_id')
    search_fields = ['entrez_gene_id', 'ensembl_gene_id']
    list_filter = ['taxid']
admin.site.register(gene2ensembl, gene2ensemblAdmin)

class EnsemblEntrezGeneIdAdmin(admin.ModelAdmin):
    list_display = ('ensembl_gene_id', 'entrez_gene_id', 'taxid')
    search_fields = ['entrez_gene_id', 'ensembl_gene_id']
    list_filter = ['taxid']
admin.site.register(EnsemblEntrezGeneId, EnsemblEntrezGeneIdAdmin)

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
admin.site.register(Gen, GenAdmin)

class OrthologAdmin(admin.ModelAdmin):
    list_display = ('ortholog', 'ortholog_symbol', 'ortholog_taxid', 'gene', 'gene_symbol', 'gene_taxid')
    search_fields = ['ortholog', 'ortholog_symbol', 'ortholog_taxid', 'gene', 'gene_symbol']
    list_filter = ['ortholog_taxid', 'gene_taxid']

admin.site.register(Ortholog, OrthologAdmin)

class Entrez_GeneAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'gene_symbol', 'gene_name', 'locus_tag', 'symbol_from_nomenclature_authority', 'full_name_from_nomenclature_autority', 'ensembl_gene_id', 'mirbase', 'mgi', 'hgnc', 'mim', 'hprd', 'rgd', 'ratmap', 'wormbase_id', 'imgt_gene_db', 'taxid')
admin.site.register(Entrez_Gene, Entrez_GeneAdmin)

##class memberAdmin(admin.ModelAdmin):
##    list_display = ('entrez_gene_id', 'mapping', 'member_id', 'stable_id', 'version', 'source_name', 'taxon_id', 'genome_db_id', 'sequence_id', 'gene_member_id', 'description', 'chr_name', 'chr_start', 'chr_end', 'chr_strand', 'display_label')
##    search_fields = ['stable_id']
##admin.site.register(member, memberAdmin)

##class homologyAdmin(admin.ModelAdmin):
##    list_display = ('homology_id', 'stable_id', 'method_link_species_set_id', 'description', 'dn', 'ds', 'n', 's', 'lnl', 'threshold_on_ds', 'ancestor_node_id', 'tree_node_id')
##    search_fields = ['homology_id']
##admin.site.register(homology, homologyAdmin)    
