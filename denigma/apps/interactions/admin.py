from django.contrib import admin

import reversion

from models import *


class AdminInteraction(admin.ModelAdmin):
    list_display = ('id_a', 'id_b', 'alias_a', 'alias_b', 'pmid')
    search_fields = ('id_a', 'id_b', 'alias_a', 'alias_b')
    list_filter = ('taxid_a', 'score')
admin.site.register(Interaction, AdminInteraction)

##class ChoiceInline(admin.TabularInline): #StackedInline
##    model = Choice
##    extra = 3


class Fly_TF_geneAdmin(admin.ModelAdmin): pass
admin.site.register(Fly_TF_gene, Fly_TF_geneAdmin)


class AdminYeastract(admin.ModelAdmin):
    list_display = ('tf', 'target_gene', 'source', 'target')
    search_fields = ['tf', 'target', 'source', 'target']
admin.site.register(Yeastract, AdminYeastract)

##    fieldsets = [
##        (None,  {'fields': ['question']}),
##        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
##    ]
##    inlines = [ChoiceInline]
##    list_display = ('question', 'pub_date', 'was_published_today')
##    list_filter = ['pub_date']
##    search_fields = ['question']
##    date_hierachy = 'pub_date'




#admin.site.register(Choice)


##class AdminBiogrid(admin.ModelAdmin):
##    list_display = ('biogrid_interaction_id', 'entrez_gene_interactor_a', 'entrez_gene_interactor_b', 'biogrid_id_interactor_a', 'biogrid_id_interactor_b', 'systematic_name_interactor_a', 'systematic_name_interactor_b', 'official_symbol_interactor_a', 'official_symbol_interactor_b', 'synonymns_interactor_a', 'synonyms_interactor_b', 'experimental_system', 'experimental_system_type', 'author', 'pubmed_id', 'organism_interactor_a', 'organism_interactor_b', 'throughput', 'score', 'modification', 'phenotypes', 'tags', 'source_database')#'qualifications'
##    search_fields = [ 'organism_interactor_a', 'organism_interactor_b', 'official_symbol_interactor_a', 'official_symbol_interactor_b', 'pubmed_id']
##admin.site.register(Biogrid, AdminBiogrid)

class ModellingAdmin(reversion.VersionAdmin):
    #list_display = ('interactor_a', 'source', 'interaction_type', 'target', 'interactor_b', 'pmid', 'taxid', 'primary', 'date')
    list_display = ('source', 'EntrezS', 'interaction_type', 'target', 'EntrezT', 'taxid', 'PubMed','is_primary', 'creation_date')
    search_fields = ('source', 'interaction_type', 'target')
    list_filter = ['taxid', 'pmid']

    def PubMed(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/pubmed/%s'>%s</a>" % (obj.pmid, obj.pmid)
    PubMed.allow_tags = True     #allow tags to a string

    def EntrezS(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>%s</a>" % (obj.interactor_a, obj.interactor_a)
    EntrezS.allow_tags = True     #allow tags to a string
    
    def EntrezT(self,obj):     #add a string from model admin method and model method
        return u"<a href='http://www.ncbi.nlm.nih.gov/gene/%s'>%s</a>" % (obj.interactor_b, obj.interactor_b)
    EntrezT.allow_tags = True     #allow tags to a string
    
##    def wiki(self,obj):     #add a string from model admin method and model method
##        return u"<a href='http://en.wikipedia.org/wiki/%s'>link</a>" % obj.gene_symbol.replace(" ","_")
##    wiki.allow_tags = True     #allow tags to a string
##    
##    def SGD(self,obj):
##        return u"<a href='http://www.yeastgenome.org/cgi-bin/locus.fpl?locus=%s'>link</a>" % obj.gene_symbol.replace(" ","_")
##    SGD.allow_tags = True    #allow tags to a string

admin.site.register(Modelling, ModellingAdmin)

class miRecordAdmin(admin.ModelAdmin):
    list_display = ('pubmed_id', 'target_gene_species_scientific', 'target_gene_species_common', 'target_gene_name', 'target_gene_refseq_acc', 'target_site_number', 'mirna_species', 'mirna_mature_id', 'mirna_regulation', 'reporter_target_gene_region', 'reporter_link_element1', 'test_method_inter', 'target_gene_mrna_level', 'original_description', 'mutation_target_region', 'post_mutation_method', 'original_description_mutation_region', 'target_site_position', 'mirna_regulation_site', 'reporter_target_site', 'reporter_link_element2', 'test_method_inter_site', 'original_description_inter_site', 'mutation_target_site', 'post_mutation_method_site', 'original_description_mutation_site', 'additional_note')
admin.site.register(miRecord, miRecordAdmin)
##
##class Interactome10090Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##    search_fields = ['interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score']
##admin.site.register(Interactome10090, Interactome10090Admin)
##class Interactome4932Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##    search_fields = ['interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score']
##admin.site.register(Interactome4932, Interactome4932Admin)
##class Interactome6239Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##    search_fields = ['interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score']
##admin.site.register(Interactome6239, Interactome6239Admin)
##class Interactome7227Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##    search_fields = ['interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score']
##admin.site.register(Interactome7227, Interactome7227Admin)
##class Interactome9606Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##    search_fields = ['interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score']
##admin.site.register(Interactome9606, Interactome9606Admin)
##
##class Fly_TF_geneAdmin(admin.ModelAdmin):
##    list_display = ('source', 'target', 'source_mapping', 'target_mapping', 'fly_tf_gene', 'fly_target_gene', 'pubmedid', 'pmid_url', 'url_factor', 'pmid_method', 'interaction_detect_methods', 'interaction_source', 'date_last_updated', 'interaction_type', 'gene_symbol', 'tf_symbol', 'data_source_url', 'data_version')
##    search_fields = ['fly_tf_gene', 'fly_target_gene', 'interaction_type', 'gene_symbol', 'tf_symbol']
##admin.site.register(Fly_TF_gene, Fly_TF_geneAdmin)

class tnetAdmin(admin.ModelAdmin):
    list_display = ('tf', 'tg')
admin.site.register(tnet, tnetAdmin)

class Yeast_TF_ChIP_chipAdmin(admin.ModelAdmin):
    list_display = ('orf', 'symbol', 'name', 'a1_mata1', 'abf1', 'abt1', 'aca1', 'ace2', 'adr1', 'aft2', 'arg80', 'arg81', 'aro80', 'arr1', 'ash1', 'ask10', 'azf1', 'bas1', 'bye1', 'cad1', 'cbf1', 'cha4', 'cin5', 'crz1', 'cst6', 'cup9', 'dal80', 'dal81', 'dal82', 'dat1', 'dig1', 'dot6', 'ecm22', 'eds1', 'fap7', 'fhl1', 'fkh1', 'fkh2', 'fzf1', 'gal3', 'gal4', 'gal80', 'gat1', 'gat3', 'gcn4', 'gcr1', 'gcr2', 'gln3', 'gts1', 'gzf3', 'haa1', 'hac1', 'hal9', 'hap1', 'hap2', 'hap3', 'hap4', 'hap5', 'hir1', 'hir2', 'hir3', 'hms1', 'hms2', 'hog1', 'hsf1', 'ifh1', 'ime1', 'ime4', 'ino2', 'ino4', 'ixr1', 'kre33', 'kss1', 'leu3', 'mac1', 'mal13', 'mal33', 'mbf1', 'mbp1', 'mcm1', 'mds3', 'met18', 'met28', 'met31', 'met32', 'met4', 'mga1', 'mig1', 'mig2', 'mig3', 'mot3', 'msn1', 'msn2', 'msn4', 'mss11', 'mth1', 'ndd1', 'ndt80', 'nnf2', 'nrg1', 'oaf1', 'opi1', 'pdc2', 'pdr1', 'pdr3', 'phd1', 'pho2', 'pho4', 'pip2', 'ppr1', 'put3', 'rap1', 'rco1', 'rcs1', 'rdr1', 'rds1', 'reb1', 'rfx1', 'rgm1', 'rgt1', 'rim101', 'rlm1', 'rlr1', 'rme1', 'rox1', 'rph1', 'rpi1', 'rpn4', 'rtg1', 'rtg3', 'rts2', 'sfl1', 'sfp1', 'sig1', 'sip3', 'sip4', 'skn7', 'sko1', 'smk1', 'smp1', 'snf1', 'snt2', 'sok2', 'spt10', 'spt2', 'spt23', 'srd1', 'stb1', 'stb2', 'stb4', 'stb5', 'stb6', 'ste12', 'stp1', 'stp2', 'stp4', 'sum1', 'sut1', 'sut2', 'swi4', 'swi5', 'swi6', 'tbs1', 'tec1', 'thi2', 'tos8', 'tye7', 'uga3', 'ume6', 'upc2', 'usv1', 'war1', 'wtm1', 'wtm2', 'xbp1', 'yap1', 'yap3', 'yap5', 'yap6', 'yap7', 'ybl054w', 'ybr239c', 'ybr267w', 'ydr026c', 'ydr049w', 'ydr266c', 'ydr520c', 'yer051w', 'yer130c', 'yer184c', 'yfl044c', 'yfl052w', 'ygr067c', 'yhp1', 'yjl206c', 'ykl222c', 'ykr064w', 'ylr278c', 'yml081w', 'ynr063w', 'yox1', 'ypr022c', 'ypr196w', 'yrr1', 'zap1', 'zms1')
    search_fields = ['orf', 'symbol', 'name']
admin.site.register(Yeast_TF_ChIP_chip, Yeast_TF_ChIP_chipAdmin)

##class Interactome10090Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##admin.site.register(Interactome10090, Interactome10090Admin)
##class Interactome4932Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##admin.site.register(Interactome4932, Interactome4932Admin)
##class Interactome6239Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##admin.site.register(Interactome6239, Interactome6239Admin)
##class Interactome7227Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##admin.site.register(Interactome7227, Interactome7227Admin)
##class Interactome9606Admin(admin.ModelAdmin):
##    list_display = ('interactor_a', 'interactor_b', 'experimental_system_type', 'interaction_type', 'interaction_detection_method', 'modification', 'pmid', 'source_database', 'score')
##admin.site.register(Interactome9606, Interactome9606Admin)

##class IntAdmin(admin.ModelAdmin):
##    list_display = ('unique_id_a', 'unique_id_b', 'alias_a', 'alias_b', 'experimental_system_type', 'interaction_type', 'experimental_system', 'modification', 'taxid_a', 'taxid_a', 'pmid', 'source_database', 'score')
##admin.site.register(Int, IntAdmin)
