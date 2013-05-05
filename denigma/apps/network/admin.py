from django.contrib import admin

from network.models import Analysis, Enrichment, Candidate


class EnrichmentAdmin(admin.ModelAdmin):
    list_display = ('term', 't', 's', 'r', 'pvalue')
    list_filter = ('analysis',)
    search_fields = ('term', 'analysis')


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


admin.site.register(Analysis)
admin.site.register(Enrichment, EnrichmentAdmin)
admin.site.register(Candidate, CandidateAdmin)