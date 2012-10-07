from django.contrib import admin

from models import *#wtcrvsyepd1, Lin2002, sip2delta_aging, sip2delta_wt, snf4delta_aging, snf4delta_wt, wt_aging


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class SignatureAdmin(admin.ModelAdmin):
    pass #
    # fields = ('name','profiles',  'transcripts', 'genes')


class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('seq_id', 'symbol', 'ratio', 'fold_change', 'pvalue', 'effect_size')
    list_filter = ('signature',)
    search_fields = ('seq_id', 'symbol')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Gene)
admin.site.register(Transcript, TranscriptAdmin)
admin.site.register(Intensity)
admin.site.register(Replicate)
admin.site.register(Contrast)
admin.site.register(Array)
admin.site.register(Probe)

##class ChoiceInline(admin.TabularInline): #StackedInline
##    model = Choice
##    extra = 3
#
#class YeastDRAdmin(admin.ModelAdmin):
#    fields = ['exp', 'ctr', 'fold_change', 'gene_symbol', 'ensembl_gene', 'entrez_gene_id', 'mapping']
#    list_display = ('exp', 'ctr', 'fold_change', 'gene_symbol', 'ensembl_gene', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_symbol', 'ensembl_gene', 'entrez_gene_id']
#    list_filter = ('mapping',)
#admin.site.register(YeastDR, YeastDRAdmin)
#
###    fieldsets = [
###        (None,  {'fields': ['question']}),
###        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
###    ]
###    inlines = [ChoiceInline]
###    list_display = ('question', 'pub_date', 'was_published_today')
###    list_filter = ['pub_date']
###    search_fields = ['question']
###    date_hierachy = 'pub_date'
#
##admin.site.register(Choice)
#
#class AdminLin2002(admin.ModelAdmin):
#    list_display = ('description', 'orf', 'gene_symbol', 'hap4oe1', 'hap4oe2', 'hxk2', 'low_glucose1', 'low_glucose2', 'entrez_gene_id', 'mapping')
#    search_fields = ['orf',
#                    'gene_symbol',
#                    'description','entrez_gene_id']
#    list_filter = ('mapping',)
#admin.site.register(Lin2002, AdminLin2002)
#
#class Adminsip2delta_wt(admin.ModelAdmin):
#    list_display = ('orf', 'gene_symbol', 'fold_change', 'description', 'main_process', 'specific_process', 'entrez_gene_id', 'mapping')
#    list_filter = ('mapping', 'main_process', 'specific_process')
#    search_fields = ['gene_symbol','orf', 'entrez_gene_id']
#admin.site.register(sip2delta_wt, Adminsip2delta_wt)
#class Adminsip2delta_aging(admin.ModelAdmin):
#    list_display = ('orf', 'gene_symbol', 'fold_change', 'description', 'main_process', 'specific_process', 'entrez_gene_id', 'mapping')
#    list_filter = ('mapping', 'main_process', 'specific_process')
#    search_fields = ['gene_symbol','orf', 'entrez_gene_id']
#admin.site.register(sip2delta_aging, Adminsip2delta_aging)
#
#class Adminsnf4delta_aging(admin.ModelAdmin):
#    list_display = ('orf', 'gene_symbol', 'fold_change', 'description', 'main_process', 'specific_process','entrez_gene_id', 'mapping')
#    list_filter = ('mapping', 'main_process', 'specific_process')
#    search_fields = ['gene_symbol','orf', 'entrez_gene_id']
#admin.site.register(snf4delta_aging, Adminsnf4delta_aging)
#class Adminsnf4delta_wt(admin.ModelAdmin):
#    list_display = ('orf', 'gene_symbol', 'fold_change', 'description', 'main_process', 'specific_process', 'entrez_gene_id', 'mapping')
#    list_filter = ('mapping', 'main_process', 'specific_process')
#    search_fields = ['gene_symbol','orf', 'entrez_gene_id']
#admin.site.register(snf4delta_wt, Adminsnf4delta_wt)
#class Adminwt_aging(admin.ModelAdmin):
#    list_display = ('orf', 'gene_symbol', 'fold_change', 'description', 'main_process', 'specific_process', 'entrez_gene_id', 'mapping')
#    list_filter = ('mapping', 'main_process', 'specific_process')
#    search_fields = ['gene_symbol','orf', 'entrez_gene_id']
#admin.site.register(wt_aging, Adminwt_aging)
#
#class RapamycinAdmin(admin.ModelAdmin):
#    list_display = ('orf', 'rapamycin_replicate_1', 'rapamycin_replicate_2', 'rapamycin_mean', 'fpr1_8_rapamycin_replicate_1', 'fpr1_8_rapamycin_replicate_2', 'fpr1_8_rapamycin_replicate_3', 'fpr1_8_rapamycin_mean', 'ly_83583_replicate_1', 'ly_83583_replicate_2', 'ly_83583_mean')
#    search_fields = ['orf','entrez_gene_id']
#admin.site.register(Rapamycin, RapamycinAdmin)
#
#class rapamycin_proteinAdmin(admin.ModelAdmin):
#    list_display = ('protein', 'fold_change', 'protein_function')
#    search_fields = ['protein','protein_function']
#admin.site.register(rapamycin_protein, rapamycin_proteinAdmin)
#
#class AgeMapAdmin(admin.ModelAdmin):
#    list_display = ('unigene',
#                    'gene_symbol',
#                    'gene_ontology',
#                     'classification',
#                    'entrez_gene_id',
#                    'mapping')
#    list_filter = ['mapping', 'classification']
#    search_fields = ['unigene',
#                    'gene_symbol',
#                    'gene_ontology',
#                    'entrez_gene_id']
#admin.site.register(AgeMap, AgeMapAdmin)
#
#class AgingSignatureAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'gene_name',
###                    'human_brain',
###                    'human_kidney',
###                    'human_muscle_1',
###                    'human_muscle_2',
###                    'mouse_brain',
###                    'mouse_cochlea',
###                    'mouse_eye',
###                    'mouse_heart',
###                    'mouse_hematopoietic',
###                    'mouse_hippocampus',
###                    'mouse_kidney',
###                    'mouse_liver',
###                    'mouse_muscle',
###                    'mouse_myoblast',
###                    'mouse_neocortex',
###                    'rat_cardiac',
###                    'rat_extraocular',
###                    'rat_glia',
###                    'rat_hippocampal_ca1_1',
###                    'rat_hippocampal_ca1_2',
###                    'rat_hippocampus',
###                    'rat_larynge',
###                    'rat_muscle',
###                    'rat_oculomotor',
###                    'rat_spinal',
###                    'rat_stromal',
#                    'n_genes',
#                    'p_value',
#                    'taxid',
#                    'classification',
#                    'entrez_gene_id',
#                    'mapping')
#    list_filter = ['mapping', 'taxid', 'classification']
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
#admin.site.register(AgingSignature, AgingSignatureAdmin)
#class AgingSignatureChiAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'gene_name',
#                    'n_genes',
#                    'p_value',
#                    'taxid',
#                    'classification',
#                    'entrez_gene_id',
#                    'mapping')
#    list_filter = ['mapping', 'taxid', 'classification']
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
#admin.site.register(AgingSignatureChi, AgingSignatureChiAdmin)
#
#class AgingLui2010Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'observation',
#                    'pubmedid',
#                    'reference',
#                    'classification',
#                    'entrez_gene_id',
#                    'mapping')
#    list_filter = ['mapping', 'classification']
#    search_fields = ['gene_symbol','entrez_gene_id']
#admin.site.register(AgingLui2010, AgingLui2010Admin)
#
#class AgingTranscriptomeAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'gene_name', 'classification', 'entrez_gene_id', 'mapping')
#    list_filter = ['mapping', 'classification']
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id', 'unigene_id', 'rna_nucleotide_accession_version']
#admin.site.register(AgingTranscriptome, AgingTranscriptomeAdmin)
#
#class Cc3Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_cc_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_cc',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping', 'cycling']
#admin.site.register(Cc3, Cc3Admin)
#
#class CdAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'scn', 'liv', 'kid', 'aor', 'skm', 'hat', 'adg', 'bat',
#                    'wat', 'bon', 'wat', 'pfr', 'wb', 'atr', 'ven',
#                    'num_tissue',
#                    'range_p',
#                    'peak_mean',
#                    'entrez_gene_id',
#                    'mapping', )
#    search_fields = ['gene_symbol', 'mapping', 'entrez_gene_id']
#    list_filter = ['mapping']
#admin.site.register(Cd, CdAdmin)
#
#class CrSignatureAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'gene_name', 'total', 'overexp', 'underexp', 'classification', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
#    list_filter = ['mapping','classification', 'overexp', 'underexp','total']
#admin.site.register(CrSignature, CrSignatureAdmin)
#
#class CrTranscriptomeAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'gene_name', 'chromosome', 'changes_in_cr', 'classification', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_name']
#    list_filter = ['mapping','classification', 'changes_in_cr','chromosome']
#admin.site.register(CrTranscriptome, CrTranscriptomeAdmin)
#
#class DdAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'affymetrix_probe_set',
#                    'anova_f_stat',
#                    'anova_pvalue',
#                    'ct_number',
#                    'genbank_accession_number',
#                    'ensembl_gene_id',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol','ensembl_gene_id']
#    list_filter = ['mapping']
#admin.site.register(Dd, DdAdmin)
#
#class Dd3Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_dd',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_gene_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping']
#admin.site.register(Dd3, Dd3Admin)
#
#class FastingInducedGenesAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'ncbi_kogs', 'locus_tag', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_symbol', 'locus_tag']
#    list_filter = ['mapping']
#admin.site.register(FastingInducedGenes, FastingInducedGenesAdmin)
#
#class ImprintedGeneNetworkAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'lung_fold_change_1_to_4wk',
###                    'lung_p_value_1_to_4wk',
#                    'lung_fold_change_1_to_8wk',
###                    'lung_p_value_1_to_8wk',
#                    'kidney_fold_change_1_to_4wk',
###                    'kidney_p_value_1_to_4wk',
#                    'kidney_fold_change_1_to_8wk',
###                    'kidney_p_value_1_to_8wk',
#                    'heart_fold_change_1_to_4wk',
###                    'heart_p_value_1_to_4wk',
#                    'consistency',
#                    'p_value',
#                    'fold_change_higher_as_5',
#                    'classification',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol',
#                    'entrez_gene_id',]
#    list_filter = [ 'mapping',
#                    'consistency',
#                    'p_value',
#                    'fold_change_higher_as_5',
#                    'classification']
#admin.site.register(ImprintedGeneNetwork, ImprintedGeneNetworkAdmin)
#
#class JuvenileInducedAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'gene_name', 'heart', 'kidney', 'lung', 'probe_set', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
#    list_filter = ['mapping']
#admin.site.register(JuvenileInduced, JuvenileInducedAdmin)
#
#class JuvenileSuppressedAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'gene_name', 'heart', 'kidney', 'lung', 'probe_set', 'entrez_gene_id', 'mapping')
#    search_fields = ['gene_symbol', 'gene_name', 'entrez_gene_id']
#    list_filter = ['mapping']
#admin.site.register(JuvenileSuppressed, JuvenileSuppressedAdmin)
#
#class LdAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'affymetrix_probe_set',
#                    'anova_f_stat',
#                    'anova_pvalue',
#                    'ct_number',
#                    'genbank_accession_number',
#                    'ensembl_gene_id',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol','ensembl_gene_id']
#    list_filter = ['mapping']
#
#admin.site.register(Ld, LdAdmin)
#
#class Ld3Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_ld',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping']
#admin.site.register(Ld3, Ld3Admin)
#
#class Lddd6Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_dd_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_ld',
#                    'fold_change_dd',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping']
#admin.site.register(Lddd6, Lddd6Admin)
#
#class PostnatalGeneticProgramAdmin(admin.ModelAdmin):
#    list_display = ('gene_symbol','classification','entrez_gene_id', 'mapping')
#    list_filter = ['mapping', 'classification']
#    search_fields = ['gene_symbol']
#admin.site.register(PostnatalGeneticProgram, PostnatalGeneticProgramAdmin)
#
#class Swindell2009Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol', 'classification', 'p_value','entrez_gene_id', 'mapping', 'NCBI', 'wiki')
#    search_fields = ['gene_symbol','entrez_gene_id']
#    list_filter = ['mapping', 'classification']
#
#    def NCBI(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.ncbi.nlm.nih.gov/gquery/?term=%s'>link</a>" % obj.gene_symbol    #http://www.ncbi.nlm.nih.gov/gene/
#    NCBI.allow_tags = True     #allow tags to a string
#
#    def wiki(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
#    wiki.allow_tags = True     #allow tags to a string
#admin.site.register(Swindell2009, Swindell2009Admin)
#
#class Wc5Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_wc',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping']
#admin.site.register(Wc5, Wc5Admin)
#
#class Wccc6Admin(admin.ModelAdmin):
#    list_display = ('gene_symbol',
#                    'fourier_f24',
#                    'fourier_pvalue',
#                    'anova_cc_f',
#                    'phase',
#                    'ac24_avg',
#                    'ac24_max',
#                    'fold_change_cc',
#                    'expression_avg',
#                    'cycling',
###                    'ws195_wormbase_goterm_info',
#                    'wormbase_id',
#                    'locus_tag',
#                    'affymetrix_probe_id_set',
#                    'entrez_gene_id',
#                    'mapping')
#    search_fields = ['gene_symbol']
#    list_filter = ['mapping']
#admin.site.register(Wccc6, Wccc6Admin)
#
#class miRNA_MSC_allAdmin(admin.ModelAdmin):
#    list_display = ('identifier', 'gene_symbol', 'aveexpr', 't', 'p_value', 'adj_p_val', 'b')
#admin.site.register(miRNA_MSC_all, miRNA_MSC_allAdmin)
#class miRNA_MSC_youngAdmin(admin.ModelAdmin):
#    list_display = ('identifier', 'gene_symbol', 'aveexpr', 't', 'p_value', 'adj_p_val', 'b')
#admin.site.register(miRNA_MSC_young, miRNA_MSC_youngAdmin)
#class miRNA_young_oldAdmin(admin.ModelAdmin):
#    list_display = ('identifier', 'gene_symbol', 'aveexpr', 't', 'p_value', 'adj_p_val', 'b')
#admin.site.register(miRNA_young_old, miRNA_young_oldAdmin)
#
#
#class WormDRAdmin(admin.ModelAdmin):
#    list_display = ('entrez_gene_id', 'mapping', 'probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'exp', 'ctr', 'fold_change')
#    search_fields = ['entrez_gene_id', 'probe_id', 'entrez_gene', 'gene_symbol', 'gene_name']
#    list_filter = ['mapping']
#admin.site.register(WormDR, WormDRAdmin)
#
#class S288c_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(S288c_caffeine, S288c_caffeineAdmin)
#class S288c_rapamycinAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(S288c_rapamycin, S288c_rapamycinAdmin)
#class Sigma2000_rapamycinAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(Sigma2000_rapamycin, Sigma2000_rapamycinAdmin)
#class Sigma2000_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(Sigma2000_caffeine, Sigma2000_caffeineAdmin)
#class W303a_0p3mM_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_0p3mM_caffeine, W303a_0p3mM_caffeineAdmin)
#class W303a_1mM_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_1mM_caffeine, W303a_1mM_caffeineAdmin)
#class W303a_1ng_mL_rapamycinAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_1ng_mL_rapamycin, W303a_1ng_mL_rapamycinAdmin)
#class W303a_200ng_mL_rapamycinAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_200ng_mL_rapamycin, W303a_200ng_mL_rapamycinAdmin)
#class W303a_3mM_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_3mM_caffeine, W303a_3mM_caffeineAdmin)
#class W303a_5ng_mL_rapamycinAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_5ng_mL_rapamycin, W303a_5ng_mL_rapamycinAdmin)
#class W303a_6mM_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_6mM_caffeine, W303a_6mM_caffeineAdmin)
#class W303a_9mM_caffeineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(W303a_9mM_caffeine, W303a_9mM_caffeineAdmin)
#
#class BY4741_rapamycin_200ng_mL_1hAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(BY4741_rapamycin_200ng_mL_1h, BY4741_rapamycin_200ng_mL_1hAdmin)
#class BY4741_rapamycin_30minAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location']
#admin.site.register(BY4741_rapamycin_30min, BY4741_rapamycin_30minAdmin)
#
#class FlyDR_trnAdmin(admin.ModelAdmin):
#    list_display = ('entrez_gene_id', 'mapping', 'probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene', 'exp', 'ctr', 'fold_change')
#    search_fields = ['entrez_gene_id','probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene']
#    list_filter = ['mapping']
#admin.site.register(FlyDR_trn, FlyDR_trnAdmin)
#
#class FlyDR_10dayAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene', 'exp', 'ctr', 'fold_change')
#    search_fields = ['probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene']
#admin.site.register(FlyDR_10day, FlyDR_10dayAdmin)
#
#class FlyDR_40dayAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene', 'exp', 'ctr', 'fold_change')
#    search_fields = ['probe_id', 'entrez_gene', 'gene_symbol', 'gene_name', 'ensembl_gene']
#admin.site.register(FlyDR_40day, FlyDR_40dayAdmin)
#
#class SpermidineAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'ensembl_gene', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'ensembl_gene', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change']
#admin.site.register(Spermidine, SpermidineAdmin)
#
#class PI3K_m_vs_hxAdmin(admin.ModelAdmin):
#    list_display = ('ensembl_id', 'wormbase', 'NCBI', 'special', 'hx546_1', 'm333_1', 'hx546_2', 'm333_2', 'hx546_3', 'm333_3', 'hx546_4', 'mg44_4', 'hx546_5', 'mg44_5', 'hx546_6', 'mg44_6', 'hx546_7', 'mg44_7', 'hx546_8', 'm333_8', 'sum_m', 'sum_hx', 'sum_all', 'expressed', 'fold_change', 'p_value')
#    search_fields = ['ensembl_id']
#
#    def NCBI(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.ncbi.nlm.nih.gov/gquery/?term=%s'>link</a>" % obj.ensembl_id    #http://www.ncbi.nlm.nih.gov/gene/
#    NCBI.allow_tags = True     #allow tags to a string
#
#    def wormbase(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.wormbase.org/db/gene/gene?name=%s;class=Gene'>link</a>" % obj.ensembl_id
#    wormbase.allow_tags = True     #allow tags to a string
#
#admin.site.register(PI3K_m_vs_hx, PI3K_m_vs_hxAdmin)
#
#class PI3K_m_vs_N2Admin(admin.ModelAdmin):
#    list_display = ('ensembl_id','wormbase', 'NCBI', 'special', 'n2_1', 'm333_1', 'n2_2', 'mg44_2', 'n2_3', 'mg44_3', 'n2_4', 'm333_4', 'n2_5', 'mg44_5', 'n2_6', 'm33_6', 'sum_m', 'sum_n2','expressed', 'fold_change', 'p_value')
#    search_fields = ['ensembl_id']
#    def NCBI(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.ncbi.nlm.nih.gov/gquery/?term=%s'>link</a>" % obj.ensembl_id    #http://www.ncbi.nlm.nih.gov/gene/
#    NCBI.allow_tags = True     #allow tags to a string
#    def wormbase(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.wormbase.org/db/gene/gene?name=%s;class=Gene'>link</a>" % obj.ensembl_id
#    wormbase.allow_tags = True     #allow tags to a string
#
#admin.site.register(PI3K_m_vs_N2, PI3K_m_vs_N2Admin)
#
#class germline_expressed_genesAdmin(admin.ModelAdmin):
#    list_display = ('ensembl_id', 'symbol', 'chr', 'germline_tags',)
#admin.site.register(germline_expressed_genes, germline_expressed_genesAdmin)
#class Germline_specific_genesAdmin(admin.ModelAdmin):
#    list_display = ('ensembl_id', 'symbol', 'germline_tags', 'in_situ', 'sage', 'microarray', 'rnai', 'descriptions')
#admin.site.register(Germline_specific_genes, Germline_specific_genesAdmin)
#
#class IME1_overexpressionAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change', 'change_1', 'change_2')
#admin.site.register(IME1_overexpression, IME1_overexpressionAdmin)
#class NDT80_knockoutAdmin(admin.ModelAdmin):
#    list_display = ('orf', 'fold_change', 'p_value')
#    search_fields = ['orf']
#admin.site.register(NDT80_knockout, NDT80_knockoutAdmin)
#class NDT80_overexpressionAdmin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#    search_fields = ['probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change']
#admin.site.register(NDT80_overexpression, NDT80_overexpressionAdmin)
#class Yeast_TF_bindingAdmin(admin.ModelAdmin):
#    list_display = ('orf', 'symbol', 'name', 'a1_mata1', 'abf1', 'abt1', 'aca1', 'ace2', 'adr1', 'aft2', 'arg80', 'arg81', 'aro80', 'arr1', 'ash1', 'ask10', 'azf1', 'bas1', 'bye1', 'cad1', 'cbf1', 'cha4', 'cin5', 'crz1', 'cst6', 'cup9', 'dal80', 'dal81', 'dal82', 'dat1', 'dig1', 'dot6', 'ecm22', 'eds1', 'fap7', 'fhl1', 'fkh1', 'fkh2', 'fzf1', 'gal3', 'gal4', 'gal80', 'gat1', 'gat3', 'gcn4', 'gcr1', 'gcr2', 'gln3', 'gts1', 'gzf3', 'haa1', 'hac1', 'hal9', 'hap1', 'hap2', 'hap3', 'hap4', 'hap5', 'hir1', 'hir2', 'hir3', 'hms1', 'hms2', 'hog1', 'hsf1', 'ifh1', 'ime1', 'ime4', 'ino2', 'ino4', 'ixr1', 'kre33', 'kss1', 'leu3', 'mac1', 'mal13', 'mal33', 'mbf1', 'mbp1', 'mcm1', 'mds3', 'met18', 'met28', 'met31', 'met32', 'met4', 'mga1', 'mig1', 'mig2', 'mig3', 'mot3', 'msn1', 'msn2', 'msn4', 'mss11', 'mth1', 'ndd1', 'ndt80', 'nnf2', 'nrg1', 'oaf1', 'opi1', 'pdc2', 'pdr1', 'pdr3', 'phd1', 'pho2', 'pho4', 'pip2', 'ppr1', 'put3', 'rap1', 'rco1', 'rcs1', 'rdr1', 'rds1', 'reb1', 'rfx1', 'rgm1', 'rgt1', 'rim101', 'rlm1', 'rlr1', 'rme1', 'rox1', 'rph1', 'rpi1', 'rpn4', 'rtg1', 'rtg3', 'rts2', 'sfl1', 'sfp1', 'sig1', 'sip3', 'sip4', 'skn7', 'sko1', 'smk1', 'smp1', 'snf1', 'snt2', 'sok2', 'spt10', 'spt2', 'spt23', 'srd1', 'stb1', 'stb2', 'stb4', 'stb5', 'stb6', 'ste12', 'stp1', 'stp2', 'stp4', 'sum1', 'sut1', 'sut2', 'swi4', 'swi5', 'swi6', 'tbs1', 'tec1', 'thi2', 'tos8', 'tye7', 'uga3', 'ume6', 'upc2', 'usv1', 'war1', 'wtm1', 'wtm2', 'xbp1', 'yap1', 'yap3', 'yap5', 'yap6', 'yap7', 'ybl054w', 'ybr239c', 'ybr267w', 'ydr026c', 'ydr049w', 'ydr266c', 'ydr520c', 'yer051w', 'yer130c', 'yer184c', 'yfl044c', 'yfl052w', 'ygr067c', 'yhp1', 'yjl206c', 'ykl222c', 'ykr064w', 'ylr278c', 'yml081w', 'ynr063w', 'yox1', 'ypr022c', 'ypr196w', 'yrr1', 'zap1', 'zms1')
#admin.site.register(Yeast_TF_binding, Yeast_TF_bindingAdmin)
#class Sporulation_2h_vs_0Admin(admin.ModelAdmin):
#    list_display = ('probe_id', 'unigene_title', 'nucleotide_title', 'go_component', 'unigene_id', 'go_component_id', 'chromosome_annotation', 'go_function', 'platform_orf', 'platform_cloneid', 'go_process_id', 'genbank_accession', 'gene_symbol', 'go_process', 'entrez_gene_id', 'gi', 'unigene_symbol', 'platform_spotid', 'go_function_id', 'gene_name', 'chromosome_location', 'fold_change')
#admin.site.register(Sporulation_2h_vs_0, Sporulation_2h_vs_0Admin)
#
#class NDT80ERAdmin(admin.ModelAdmin):
#    list_display = ('orf', 'ndt80_9h_1_pvalue', 'ndt80_9h_1_ratio', 'ndt80_9h_2_pvalue', 'ndt80_9h_2_ratio', 'avearge_ratio_ndt80_9h', 'ndt80_zscore', 'ndt80_binding_zscore_077', 'ndt80_site', 'sum1_15h_1_pvalue', 'sum1_15h_1_ratio', 'sum1_15h_2_pvalue', 'sum1_15h_2_ratio', 'avearge_sum1_15h', 'sum1zscore', 'sum1_binding', 'sum1_site', 'ndt80_only', 'common', 'sum1_only', 'harbison_2004_sum1_chip_on_chip_in_ypd_pvalue', 'wang_2005_ndt80_tar', 'wang_2005_sum1_tar', 'pierce_2003_sum1_derepressed', 'chu_1998_over_2_in_ndt80oe', 'primig_2000_cluster1', 'primig_2000_cluster2', 'primig_2000_cluster3', 'primig_2000_cluster4', 'primig_2000_cluster5', 'primig_2000_cluster6', 'primig_2000_cluster7', 'primig_2000_cluster8', 'primig_2000_cluster9', 'primig_2000_cluster10', 'mrna_0h', 'mrna_1h', 'mrna_2h', 'mrna_3h', 'mrna_4h', 'mrna_5h', 'mrna_6h', 'mrna_7h', 'mrna_8h', 'mrna_9h', 'mrna_10h', 'mrna_11h', 'mrna_12h', 'mrna_13h', 'mrna_14h', 'mrna_15h', 'mrna_16h', 'mrna_17h', 'mrna_18h', 'cluster', 'before_deconvolution_0h', 'before_deconvolution_14', 'before_deconvolution_18', 'sum1_deletion_10h', 'sum1_deletion_17h', 'sum1_deletion_21h', 'ndt80er_0h', 'ndt80er_8h', 'ndt80er_14h')
#admin.site.register(NDT80ER, NDT80ERAdmin)
#
#class PI3KAdmin(admin.ModelAdmin):
#    list_display = ('ensembl_id',
#                    'entrez_gene_id',
#                    'symbol',
#                    'name',
#                    'wormbase',
#                    'NCBI',
#                    'special',
#                    'N2_sum',
#                    'N2_average',
#                    'N2_variance',
#                    'hx_sum',
#                    'hx_average',
#                    'hx_variance',
#                    'm_sum',
#                    'm_average',
#                    'm_variance',
#                    'expressed',
#                    'hx_N2_fold_change',
#                    'hx_N2_p_value',
#                    'm_hx_fold_change',
#                    'm_hx_p_value',
#                    'm_N2_fold_change',
#                    'm_N2_p_value')
#    search_fields = ['entrez_gene_id','ensembl_id', 'symbol', 'name']
#    def NCBI(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.ncbi.nlm.nih.gov/gquery/?term=%s'>link</a>" % obj.ensembl_id    #http://www.ncbi.nlm.nih.gov/gene/
#    NCBI.allow_tags = True     #allow tags to a string
#    def wormbase(self,obj):     #add a string from model admin method and model method
#        return u"<a href='http://www.wormbase.org/db/gene/gene?name=%s;class=Gene'>link</a>" % obj.ensembl_id
#    wormbase.allow_tags = True     #allow tags to a string
#
#admin.site.register(PI3K, PI3KAdmin)
#
#class TemporalLinkageDRAdmin(admin.ModelAdmin):
#    list_display = ('genbank', 'symbol', 'cr2', 'cr4', 'cr8', 'lt_cr', 'con8', 'gene_class', 'category')
#    search_fields = ['genbank', 'symbol']
#    list_filter = ['gene_class', 'category']
#admin.site.register(TemporalLinkageDR, TemporalLinkageDRAdmin)
#
#class CeMMAdmin(admin.ModelAdmin):
#    list_display = ('ensembl', 'array_1', 'array_2', 'array_3')
#    search_fields = ['ensembl']
#admin.site.register(CeMM, CeMMAdmin)
#
#
#class AlteredGeneExpressionInCeMMAdmin(admin.ModelAdmin):
#    list_display = ('fold_change', 'ensembl', 'mountain', 'description', 'regulation')
#    search_fields = ['ensembl', 'description']
#    list_filter = [ 'regulation', 'mountain']
#admin.site.register(AlteredGeneExpressionInCeMM, AlteredGeneExpressionInCeMMAdmin)
