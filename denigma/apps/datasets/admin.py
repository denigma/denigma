from datasets.models import *#Gendr, Ultradian, Adult_Height_Association, BMAL1_Sites_Liver
from django.contrib import admin

import reversion



admin.site.register(Signature)


class GendrAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol','gene_name', 'alias', 'taxid', 'observation', 'pubmed_id', 'reference', 'classification', 'ensembl_gene_id', 'entrez_gene_id', 'mapping')
    search_fields = ['gene_symbol','gene_name','alias', 'entrez_gene_id', 'pubmed_id', 'reference']
    list_filter = ('mapping', 'taxid', 'classification')
admin.site.register(Gendr, GendrAdmin)


class ReferenceAdmin(reversion.VersionAdmin):
    list_display = ('pmid', 'title', 'author', 'year', 'journal', 'full_text')# 'title', 'journal', 'publication_date')#'year'
    list_filter = ['year']
    #fields = ('pmid', 'title', 'authors', 'year', 'research_notes')
    #raw_id_fields = ('intervention',)
##    list_filter = ('publication_date',)
##    date_hierarchy = 'publication_date'
##    ordering = ('-publication_date',)
##    fields = ('title', 'authors', 'publisher', 'publication_date')
##    filter_horizontal = ('authors',)
##    raw_id_fields = ('publisher',)
    list_search = ['pmid', 'year', ]
    search_fields = ['title', 'pmid', 'authors', 'year']

    def author(self, obj):
        if not obj.authors:
           return ""
        authors = obj.authors.split(' ')
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
           return "%s & %s" % (authors[0], authors[1])
        else:
           return "%s et al." % authors[0]
    author.allow_tags = True

    def full_text(self, obj):
        if obj.link:
            return '<a href="%s">%s</a>' % (obj.link, 'available')
        else:
            return 'not linked'
    full_text.allow_tags = True
##
##    def first_names(self, obj): #Note that this method can also be on the Model not just ModelAdmin
##        return ','.join(a.first_name for a in obj.authors.all())    #http://stackoverflow.com/questions/2861923/how-do-i-reference-django-model-from-another-model
##    get_sites.short_description = 'First Names'
admin.site.register(Reference, ReferenceAdmin)



class ChangeAdmin(reversion.VersionAdmin):
    list_display = ('name', 'description', 'gender', 'comparision', 'start', 'stop', 'tissue', 'pmid', 'reference', 'taxid')
    list_filter = ['comparision', 'taxid', 'tissue']
    search_fields = ['name', 'pmid', 'reference']
    fields = ('name', 'description', 'taxid', 'tissue', 'gender', 'comparision',  'start', 'stop',  'pmid', 'reference',  'references')
    filter_horizontal = ('references',)
admin.site.register(Change, ChangeAdmin)


class AdminUltradian(admin.ModelAdmin):
    list_display = ('orf', 'gene', 'description', 'process', 'component', 'function', 'f', 'o')
admin.site.register(Ultradian, AdminUltradian)

class AdminAdult_Height_Association(admin.ModelAdmin):
    list_display = ('locus_rank', 'chr', 'gene_symbol', 'snp', 'effect_allele', 'male_effect', 'male_p', 'female_effect', 'female_p', 'phet_m_vs_f')
admin.site.register(Adult_Height_Association, AdminAdult_Height_Association)

class AdminBMAL1_Sites_Liver(admin.ModelAdmin):
    list_display = ('chromosome', 'start', 'end', 'distance', 'gene_symbol', 'biotype', 'mrna_pvalue', 'mrna_phase', 'e1', 'e1_e2', 'conservation', 'zt2', 'zt6', 'zt10', 'zt14', 'zt18', 'zt22')
    search_fields = ['gene_symbol']
    list_filter = ('chromosome', 'biotype')
admin.site.register(BMAL1_Sites_Liver, AdminBMAL1_Sites_Liver)

class DAM_Fernandez2011Admin(admin.ModelAdmin):
    list_display = ('cpg_site', 'cgi', 'gene_symbol', 'correlation', 'p_value')
    search_fields = ['cpg_site', 'cgi', 'gene_symbol']
admin.site.register(DAM_Fernandez2011, DAM_Fernandez2011Admin)

class GenCCAdmin(reversion.VersionAdmin):
    list_display = ('entrez_gene_id', 'mapping', 'gene_symbol', 'alias', 'taxid', 'function', 'observation', 'pubmed_id', 'reference', 'classification', 'peak_mrna', 'peak_protein', 'peak_actvity')
    search_fields = ['entrez_gene_id', 'gene_symbol', 'alias']
    list_filter = ['mapping',
                    'classification',
                    'taxid']
admin.site.register(GenCC, GenCCAdmin)

class AdultHeightAssociationAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'mapping', 'locus_rank', 'chr', 'gene_symbol', 'snp', 'effect_allele', 'male_effect', 'male_p', 'female_effect', 'female_p', 'phet_m_vs_f')
    list_filter = ['mapping', 'effect_allele', 'male_effect', 'female_effect']
    search_fields = ['entrez_gene_id', 'gene_symbol']
admin.site.register(AdultHeightAssociation, AdultHeightAssociationAdmin)

class CircadianSystemicEntrainedFactorsAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol', 'alias', 'entrez_gene_id', 'mapping')
    search_fields = ['gene_symbol']
    list_filter = ['mapping']
admin.site.register(CircadianSystemicEntrainedFactors, CircadianSystemicEntrainedFactorsAdmin)

class ClockModulatorAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol',
                    'gene_name',
                    'phenotype',
                    'confirmed_by_bmal1_kockdown',
                    'rna_nucleotide_accession_version',
                    'entrez_gene_id', 'mapping')
    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
    list_filter = ['mapping']
admin.site.register(ClockModulator, ClockModulatorAdmin)

class HumanGenesAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol',
                    'gene_name',
                    'selection_reason',
##                    'band',
##                    'location_start',
##                    'location_end',
##                    'orientation',
##                    'function',
##                    'cellular_location',
##                    'omim',
##                    'hprd',
##                    'unigene',
                    'entrez_gene_id',
##                    'homologene',
##                    'swiss_prot',
##                    'interactions',
##                    'homologues',
##                    'reference',
##                    'pubmed_ids'
                    'mapping')
    #'hagrid','aliases','observations','epd_accession','orf_accession','cds_accession',                    'expression',
    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id', 'reference']
    list_filter = ['mapping']
admin.site.register(HumanGenes, HumanGenesAdmin)

class JoanneGenesAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol',
                     'assoc_gene_name',
                     'ensembl_gene_id',
                     'dn',
                     'ds',
                     'dn_ds',
                     'human_percentage_id',
                     'chimp_percentage_id',
                     'cds_length',
                     'longevity',
                    'entrez_gene_id',
                    'mapping')
    search_fields = ['gene_symbol',
                     'assoc_gene_name',
                     'ensembl_gene_id',]
    list_filter = ['mapping']
admin.site.register(JoanneGenes, JoanneGenesAdmin)

class MurineImprintedAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol',
                    'chromosome',
                    'chromosome_region',
                    'expressed_parental_allele',
                    'gene_name',
                    'classification',
                    'entrez_gene_id',
                    'mapping')
    list_filter = ['mapping',
                   'chromosome',
                   'chromosome_region',
                   'expressed_parental_allele',
                   'classification']
    search_fields = ['gene_symbol', 'gene_name']
admin.site.register(MurineImprinted, MurineImprintedAdmin)

class NewLongevityRegulatorsAdmin(admin.ModelAdmin):
    list_display = ('wormbase_id', 'entrez_gene_id', 'mapping', 'classification')
    search_fields = ['wormbase_id', 'entrez_gene_id']
    list_filter = ['mapping', 'classification']
admin.site.register(NewLongevityRegulators, NewLongevityRegulatorsAdmin)

class NewLongevityRegulatorsCandidatesAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol', 'ensembl_gene_id', 'wormbase_id', 'entrez_gene_id', 'mapping')
    search_fields = ['wormbase_id', 'entrez_gene_id', 'ensembl_gene_id', 'gene_symbol']
    list_filter = ['mapping']
admin.site.register(NewLongevityRegulatorsCandidates, NewLongevityRegulatorsCandidatesAdmin)

class SurvivingInTheColdAdmin(admin.ModelAdmin):
    list_display = ('locus_tag',
                    'protein_accession_number',
                    'sgd_id',
                    'embl',
                    'entrez_gene_id',
                    'mapping')
    search_fields = ['Locus_tag','entrez_gene_id', 'sgd_id', 'embl']
    list_filter = ['mapping']
admin.site.register(SurvivingInTheCold, SurvivingInTheColdAdmin)

class HumanBrainDnaMethylationChangesAdmin(admin.ModelAdmin):
    list_display = ('gene_symbol', 'chr', 'genomic_position_in_bp', 'distance_to_tss', 'entrez_gene_id', 'mapping', 'NCBI', 'wiki')

    def NCBI(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>link</a>" % obj.entrez_gene_id
    NCBI.allow_tags = True     #allow tags to a string
    
    def wiki(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
    wiki.allow_tags = True     #allow tags to a string
admin.site.register(HumanBrainDnaMethylationChanges, HumanBrainDnaMethylationChangesAdmin)

class K56AcAdmin(admin.ModelAdmin):
    list_display = ('ensembl_gene', 'level', 'expression')
admin.site.register(K56Ac, K56AcAdmin)

class PokholokAdmin(admin.ModelAdmin):
    list_display = ('ensembl_gene', 'chr', 'pos', 'h3_ypd', 'h4_ypd', 'h3_h2o2', 'h3k9acvsh3_ypd', 'h3k14acvsh3_ypd', 'h3k14acvswce_ypd', 'h3k14acvsh3_h2o2', 'h4acvsh3_ypd', 'h4acvsh3_h2o2', 'h3k4me1vsh3_ypd', 'h3k4me2vsh3_ypd', 'h3k4me3vsh3_ypd', 'h3k36me3vsh3_ypd', 'h3k79me3vsh3_ypd', 'esa1_ypd', 'gcn5_ypd', 'gcn4_aa', 'gg_ypd', 'noab_ypd')
admin.site.register(Pokholok, PokholokAdmin)

class AcetylationAdmin(admin.ModelAdmin):
    list_display = ('ensembl_gene', 'h4k8', 'h4k12', 'h4k16', 'h3k9', 'h3k14', 'h3k18', 'h3k23', 'h3k27', 'h2ak7', 'h2bk11', 'h2bk16')
admin.site.register(Acetylation, AcetylationAdmin)



class HumanBrainMethylationChangesAdmin(admin.ModelAdmin):
    list_display = ('name', 'chr', 'genomic_position_in_bp', 'symbol', 'distance_to_tss', 'stage_i_p_value_crblm', 'stage_i_p_value_fctx', 'stage_i_p_value_pons', 'stage_i_p_value_tctx', 'stage_ii_p_value_crblm', 'stage_ii_p_value_fctx', 'beta_coefficient_range', 'adjusted_r2_estimates_from_stage_i_crblm', 'adjusted_r2_estimates_from_stage_i_fctx', 'adjusted_r2_estimates_from_stage_i_pons', 'adjusted_r2_estimates_from_stage_i_tctx')
admin.site.register(HumanBrainMethylationChanges, HumanBrainMethylationChangesAdmin)

class OneyrCbSpecificAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(OneyrCbSpecific, OneyrCbSpecificAdmin)
class OneyrHippSpecificAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(OneyrHippSpecific, OneyrHippSpecificAdmin)
class AdultCbDynamicAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(AdultCbDynamic, AdultCbDynamicAdmin)
class AdultCbStableAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(AdultCbStable, AdultCbStableAdmin)
class AdultHippDynamicAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(AdultHippDynamic, AdultHippDynamicAdmin)
class AdultHippStableAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(AdultHippStable, AdultHippStableAdmin)
class CbSpecificAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(CbSpecific, CbSpecificAdmin)
class HippSpecificAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(HippSpecific, HippSpecificAdmin)
class P7CbDynamicAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(P7CbDynamic, P7CbDynamicAdmin)
class P7HippDynamicAdmin(admin.ModelAdmin):
    list_display = ('chr', 'start', 'end', 'peak', 'p_value')
admin.site.register(P7HippDynamic, P7HippDynamicAdmin)
class DR_EssentialAdmin(admin.ModelAdmin):
    list_display = ('entrez_gene_id', 'gene_symbol', 'taxid', 'classification')
    list_filter = ['taxid']
admin.site.register(DR_Essential, DR_EssentialAdmin)




