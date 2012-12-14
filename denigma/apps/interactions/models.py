from django.db import models


class Interaction(models.Model):
    id_a = models.IntegerField()
    id_b = models.IntegerField()
    alias_a = models.TextField() #CharField(max_length=300, blank=True)
    alias_b = models.TextField() #CharField(max_length=300, blank=True)
    system = models.CharField(max_length=38, blank=True)
    type = models.CharField(max_length=259, blank=True) # Perhaps text field here.
    method = models.CharField(max_length=240, blank=True)
    modification = models.CharField(max_length=78, blank=True)
    taxid_a = models.IntegerField()
    taxid_b = models.IntegerField()
    pmid = models.TextField(blank=True)#CharField(max_length=255, blank=True)
    source = models.CharField(max_length=73)
    score = models.IntegerField()


##class Biogrid(models.Model):
##    biogrid_interaction_id = models.IntegerField(primary_key=True)
##    entrez_gene_interactor_a = models.IntegerField()
##    entrez_gene_interactor_b = models.IntegerField()
##    biogrid_id_interactor_a = models.IntegerField()
##    biogrid_id_interactor_b = models.IntegerField()
##    systematic_name_interactor_a = models.CharField(max_length=24)
##    systematic_name_interactor_b = models.CharField(max_length=25)
##    official_symbol_interactor_a = models.CharField(max_length=21)
##    official_symbol_interactor_b = models.CharField(max_length=31)
##    synonymns_interactor_a = models.TextField()
##    synonyms_interactor_b = models.TextField()
##    experimental_system = models.CharField(max_length=29)
##    experimental_system_type = models.CharField(max_length=8)
##    author = models.CharField(max_length=37)
##    pubmed_id = models.IntegerField()
##    organism_interactor_a = models.IntegerField()
##    organism_interactor_b = models.IntegerField()
##    throughput = models.CharField(max_length=30)
##    score = models.FloatField()
##    modification = models.CharField(max_length=22)
##    phenotypes = models.CharField(max_length=209)
##    qualifications = models.TextField()
##    tags = models.CharField(max_length=1)
##    source_database = models.CharField(max_length=7)
##    def __unicode__(self):
##        return u'%s %s'% (self.official_symbol_interactor_a, self.official_symbol_interactor_b)

class miRecord(models.Model):
    pubmed_id = models.IntegerField()
    target_gene_species_scientific = models.CharField(max_length=34, blank=True)
    target_gene_species_common = models.CharField(max_length=10, blank=True)
    target_gene_name = models.CharField(max_length=44, blank=True)
    target_gene_refseq_acc = models.CharField(max_length=14, blank=True)
    target_site_number = models.IntegerField(blank=True)
    mirna_species = models.CharField(max_length=37, blank=True)
    mirna_mature_id = models.CharField(max_length=18, blank=True)
    mirna_regulation = models.CharField(max_length=66, blank=True)
    reporter_target_gene_region = models.CharField(max_length=26, blank=True)
    reporter_link_element1 = models.CharField(max_length=24, blank=True)
    test_method_inter = models.CharField(max_length=34, blank=True)
    target_gene_mrna_level = models.CharField(max_length=9, blank=True)
    original_description = models.TextField(blank=True)
    mutation_target_region = models.CharField(max_length=3, blank=True)
    post_mutation_method = models.CharField(max_length=3, blank=True)
    original_description_mutation_region = models.TextField(blank=True)
    target_site_position = models.CharField(max_length=10, blank=True)
    mirna_regulation_site = models.CharField(max_length=63, blank=True)
    reporter_target_site = models.CharField(max_length=26, blank=True)
    reporter_link_element2 = models.CharField(max_length=25, blank=True)
    test_method_inter_site = models.CharField(max_length=27, blank=True)
    original_description_inter_site = models.TextField(blank=True)
    mutation_target_site = models.CharField(max_length=3, blank=True)
    post_mutation_method_site = models.CharField(max_length=27, blank=True)
    original_description_mutation_site = models.TextField(blank=True)
    additional_note = models.CharField(max_length=141, blank=True)

    def __unicode__(self):
        return u"{0} - {1}".format(self.mirna_mature_id, self.target_gene_name)

    class Meta:
       verbose_name = "miRecord"


class Modelling(models.Model):
    interactor_a = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=25, blank=True)
    interaction_type = models.CharField(max_length=159, blank=True)
    target = models.CharField(max_length=25, blank=True)
    interactor_b = models.IntegerField(null=True, blank=True)
    pmid = models.IntegerField(blank=True, null=True)
    taxid = models.IntegerField(null=True, blank=True)
    is_primary = models.BooleanField()
    creation_date = models.DateField(blank=True, null=True)
##    website = models.URLField()

    def __unicode__(self):
        return u'%s, %s' % (self.source, self.target)

    class Meta:
        verbose_name_plural = "modelling"


class Fly_TF_gene(models.Model):
    fly_tf_gene = models.CharField(max_length=11)
    fly_target_gene = models.CharField(max_length=11)
    pubmedid = models.CharField(max_length=33)
    pmid_url = models.CharField(max_length=119)
    url_factor = models.CharField(max_length=67)
    pmid_method = models.CharField(max_length=168)
    interaction_detect_methods = models.CharField(max_length=1, blank=True) #Delete, its empty
    interaction_source = models.CharField(max_length=36)
    date_last_updated = models.CharField(max_length=9)
    interaction_type = models.CharField(max_length=10)
    gene_symbol = models.CharField(max_length=29)
    tf_symbol = models.CharField(max_length=13)
    data_source_url = models.CharField(max_length=67)
    data_version = models.CharField(max_length=10)
    source = models.IntegerField(blank=True)
    target = models.IntegerField(blank=True)
    source_mapping = models.IntegerField(blank=True, null=True)
    target_mapping = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "{0} - {1}".format(self.tf_symbol, self.gene_symbol)

    class Meta:
       verbose_name = "fly TF - gene"


##class Interactome10090(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=38, blank=True)
##    interaction_type = models.CharField(max_length=159, blank=True)
##    interaction_detection_method = models.CharField(max_length=240, blank=True)
##    modification = models.CharField(max_length=50, blank=True)
##    pmid = models.CharField(max_length=115, blank=True)
##    source_database = models.CharField(max_length=73)
##    score = models.IntegerField()

##class Interactome4932(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=54, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.TextField()
##    score = models.IntegerField()
##
##class Interactome6239(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.CharField(max_length=174, blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=32, blank=True)
##    pmid = models.CharField(max_length=94, blank=True)
##    source_database = models.CharField(max_length=104)
##    score = models.IntegerField()
##
##class Interactome7227(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=35, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.CharField(max_length=95)
##    score = models.IntegerField()
##
##class Interactome9606(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=88, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.CharField(max_length=134)
##    score = models.IntegerField()


class tnet(models.Model):
    tf = models.CharField(max_length=7)
    tg = models.CharField(max_length=8)

    def __unicode__(self):
        return "{0} {1}".format(self.tf, self.tg)

    class Meta:
       verbose_name_plural = "Tnet"


class Yeast_TF_ChIP_chip(models.Model):
    orf = models.CharField(max_length=31, blank=True)
    symbol = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=148, blank=True)
    a1_mata1 = models.FloatField(blank=True)
    abf1 = models.FloatField(blank=True)
    abt1 = models.FloatField(blank=True)
    aca1 = models.FloatField(blank=True)
    ace2 = models.FloatField(blank=True)
    adr1 = models.FloatField(blank=True)
    aft2 = models.FloatField(blank=True)
    arg80 = models.FloatField(blank=True)
    arg81 = models.FloatField(blank=True)
    aro80 = models.FloatField(blank=True)
    arr1 = models.FloatField(blank=True)
    ash1 = models.FloatField(blank=True)
    ask10 = models.FloatField(blank=True)
    azf1 = models.FloatField(blank=True)
    bas1 = models.FloatField(blank=True)
    bye1 = models.FloatField(blank=True)
    cad1 = models.FloatField(blank=True)
    cbf1 = models.FloatField(blank=True)
    cha4 = models.FloatField(blank=True)
    cin5 = models.FloatField(blank=True)
    crz1 = models.FloatField(blank=True)
    cst6 = models.FloatField(blank=True)
    cup9 = models.FloatField(blank=True)
    dal80 = models.FloatField(blank=True)
    dal81 = models.FloatField(blank=True)
    dal82 = models.FloatField(blank=True)
    dat1 = models.FloatField(blank=True)
    dig1 = models.FloatField(blank=True)
    dot6 = models.FloatField(blank=True)
    ecm22 = models.FloatField(blank=True)
    eds1 = models.FloatField(blank=True)
    fap7 = models.FloatField(blank=True)
    fhl1 = models.FloatField(blank=True)
    fkh1 = models.FloatField(blank=True)
    fkh2 = models.FloatField(blank=True)
    fzf1 = models.FloatField(blank=True)
    gal3 = models.FloatField(blank=True)
    gal4 = models.FloatField(blank=True)
    gal80 = models.FloatField(blank=True)
    gat1 = models.FloatField(blank=True)
    gat3 = models.FloatField(blank=True)
    gcn4 = models.FloatField(blank=True)
    gcr1 = models.FloatField(blank=True)
    gcr2 = models.FloatField(blank=True)
    gln3 = models.FloatField(blank=True)
    gts1 = models.FloatField(blank=True)
    gzf3 = models.FloatField(blank=True)
    haa1 = models.FloatField(blank=True)
    hac1 = models.FloatField(blank=True)
    hal9 = models.FloatField(blank=True)
    hap1 = models.FloatField(blank=True)
    hap2 = models.FloatField(blank=True)
    hap3 = models.FloatField(blank=True)
    hap4 = models.FloatField(blank=True)
    hap5 = models.FloatField(blank=True)
    hir1 = models.FloatField(blank=True)
    hir2 = models.FloatField(blank=True)
    hir3 = models.FloatField(blank=True)
    hms1 = models.FloatField(blank=True)
    hms2 = models.FloatField(blank=True)
    hog1 = models.FloatField(blank=True)
    hsf1 = models.FloatField(blank=True)
    ifh1 = models.FloatField(blank=True)
    ime1 = models.FloatField(blank=True)
    ime4 = models.FloatField(blank=True)
    ino2 = models.FloatField(blank=True)
    ino4 = models.FloatField(blank=True)
    ixr1 = models.FloatField(blank=True)
    kre33 = models.FloatField(blank=True)
    kss1 = models.FloatField(blank=True)
    leu3 = models.FloatField(blank=True)
    mac1 = models.FloatField(blank=True)
    mal13 = models.FloatField(blank=True)
    mal33 = models.FloatField(blank=True)
    mbf1 = models.FloatField(blank=True)
    mbp1 = models.FloatField(blank=True)
    mcm1 = models.FloatField(blank=True)
    mds3 = models.FloatField(blank=True)
    met18 = models.FloatField(blank=True)
    met28 = models.FloatField(blank=True)
    met31 = models.FloatField(blank=True)
    met32 = models.FloatField(blank=True)
    met4 = models.FloatField(blank=True)
    mga1 = models.FloatField(blank=True)
    mig1 = models.FloatField(blank=True)
    mig2 = models.FloatField(blank=True)
    mig3 = models.FloatField(blank=True)
    mot3 = models.FloatField(blank=True)
    msn1 = models.FloatField(blank=True)
    msn2 = models.FloatField(blank=True)
    msn4 = models.FloatField(blank=True)
    mss11 = models.FloatField(blank=True)
    mth1 = models.FloatField(blank=True)
    ndd1 = models.FloatField(blank=True)
    ndt80 = models.FloatField(blank=True)
    nnf2 = models.FloatField(blank=True)
    nrg1 = models.FloatField(blank=True)
    oaf1 = models.FloatField(blank=True)
    opi1 = models.FloatField(blank=True)
    pdc2 = models.FloatField(blank=True)
    pdr1 = models.FloatField(blank=True)
    pdr3 = models.FloatField(blank=True)
    phd1 = models.FloatField(blank=True)
    pho2 = models.FloatField(blank=True)
    pho4 = models.FloatField(blank=True)
    pip2 = models.FloatField(blank=True)
    ppr1 = models.FloatField(blank=True)
    put3 = models.FloatField(blank=True)
    rap1 = models.FloatField(blank=True)
    rco1 = models.FloatField(blank=True)
    rcs1 = models.FloatField(blank=True)
    rdr1 = models.FloatField(blank=True)
    rds1 = models.FloatField(blank=True)
    reb1 = models.FloatField(blank=True)
    rfx1 = models.FloatField(blank=True)
    rgm1 = models.FloatField(blank=True)
    rgt1 = models.FloatField(blank=True)
    rim101 = models.FloatField(blank=True)
    rlm1 = models.FloatField(blank=True)
    rlr1 = models.FloatField(blank=True)
    rme1 = models.FloatField(blank=True)
    rox1 = models.FloatField(blank=True)
    rph1 = models.FloatField(blank=True)
    rpi1 = models.FloatField(blank=True)
    rpn4 = models.FloatField(blank=True)
    rtg1 = models.FloatField(blank=True)
    rtg3 = models.FloatField(blank=True)
    rts2 = models.FloatField(blank=True)
    sfl1 = models.FloatField(blank=True)
    sfp1 = models.FloatField(blank=True)
    sig1 = models.FloatField(blank=True)
    sip3 = models.FloatField(blank=True)
    sip4 = models.FloatField(blank=True)
    skn7 = models.FloatField(blank=True)
    sko1 = models.FloatField(blank=True)
    smk1 = models.FloatField(blank=True)
    smp1 = models.FloatField(blank=True)
    snf1 = models.FloatField(blank=True)
    snt2 = models.FloatField(blank=True)
    sok2 = models.FloatField(blank=True)
    spt10 = models.FloatField(blank=True)
    spt2 = models.FloatField(blank=True)
    spt23 = models.FloatField(blank=True)
    srd1 = models.FloatField(blank=True)
    stb1 = models.FloatField(blank=True)
    stb2 = models.FloatField(blank=True)
    stb4 = models.FloatField(blank=True)
    stb5 = models.FloatField(blank=True)
    stb6 = models.FloatField(blank=True)
    ste12 = models.FloatField(blank=True)
    stp1 = models.FloatField(blank=True)
    stp2 = models.FloatField(blank=True)
    stp4 = models.FloatField(blank=True)
    sum1 = models.FloatField(blank=True)
    sut1 = models.FloatField(blank=True)
    sut2 = models.FloatField(blank=True)
    swi4 = models.FloatField(blank=True)
    swi5 = models.FloatField(blank=True)
    swi6 = models.FloatField(blank=True)
    tbs1 = models.FloatField(blank=True)
    tec1 = models.FloatField(blank=True)
    thi2 = models.FloatField(blank=True)
    tos8 = models.FloatField(blank=True)
    tye7 = models.FloatField(blank=True)
    uga3 = models.FloatField(blank=True)
    ume6 = models.FloatField(blank=True)
    upc2 = models.FloatField(blank=True)
    usv1 = models.FloatField(blank=True)
    war1 = models.FloatField(blank=True)
    wtm1 = models.FloatField(blank=True)
    wtm2 = models.FloatField(blank=True)
    xbp1 = models.FloatField(blank=True)
    yap1 = models.FloatField(blank=True)
    yap3 = models.FloatField(blank=True)
    yap5 = models.FloatField(blank=True)
    yap6 = models.FloatField(blank=True)
    yap7 = models.FloatField(blank=True)
    ybl054w = models.FloatField(blank=True)
    ybr239c = models.FloatField(blank=True)
    ybr267w = models.FloatField(blank=True)
    ydr026c = models.FloatField(blank=True)
    ydr049w = models.FloatField(blank=True)
    ydr266c = models.FloatField(blank=True)
    ydr520c = models.FloatField(blank=True)
    yer051w = models.FloatField(blank=True)
    yer130c = models.FloatField(blank=True)
    yer184c = models.FloatField(blank=True)
    yfl044c = models.FloatField(blank=True)
    yfl052w = models.FloatField(blank=True)
    ygr067c = models.FloatField(blank=True)
    yhp1 = models.FloatField(blank=True)
    yjl206c = models.FloatField(blank=True)
    ykl222c = models.FloatField(blank=True)
    ykr064w = models.FloatField(blank=True)
    ylr278c = models.FloatField(blank=True)
    yml081w = models.FloatField(blank=True)
    ynr063w = models.FloatField(blank=True)
    yox1 = models.FloatField(blank=True)
    ypr022c = models.FloatField(blank=True)
    ypr196w = models.FloatField(blank=True)
    yrr1 = models.FloatField(blank=True)
    zap1 = models.FloatField(blank=True)
    zms1 = models.FloatField(blank=True)

    def __unicode__(self):
        return self.orf

    class Meta:
        verbose_name = "yeast TF ChIP-chip"
        verbose_name_plural = verbose_name


##class Interactome10090(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=38, blank=True)
##    interaction_type = models.CharField(max_length=159, blank=True)
##    interaction_detection_method = models.CharField(max_length=240, blank=True)
##    modification = models.CharField(max_length=50, blank=True)
##    pmid = models.CharField(max_length=115, blank=True)
##    source_database = models.CharField(max_length=73)
##    score = models.IntegerField()
##
##class Interactome4932(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=54, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.TextField()
##    score = models.IntegerField()
##
##class Interactome6239(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.CharField(max_length=174, blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=32, blank=True)
##    pmid = models.CharField(max_length=94, blank=True)
##    source_database = models.CharField(max_length=104)
##    score = models.IntegerField()
##
##class Interactome7227(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=35, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.CharField(max_length=129)
##    score = models.IntegerField()
##
##class Interactome9606(models.Model):
##    interactor_a = models.IntegerField()
##    interactor_b = models.IntegerField()
##    experimental_system_type = models.CharField(max_length=36, blank=True)
##    interaction_type = models.TextField(blank=True)
##    interaction_detection_method = models.TextField(blank=True)
##    modification = models.CharField(max_length=88, blank=True)
##    pmid = models.TextField(blank=True)
##    source_database = models.CharField(max_length=134)
##    score = models.IntegerField()


class Yeastract(models.Model):
    tf = models.CharField(max_length=7)
    tf_ensembl_id = models.CharField(max_length=9)
    target_gene = models.CharField(max_length=9)
    target_ensembl_id = models.CharField(max_length=9)
    taxid = 4932
    source = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    source_mapping = models.IntegerField(blank=True, null=True)
    target_mapping = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.tf_ensembl_id

    class Meta:
        verbose_name = "YEASTRACT"
        verbose_name_plural = verbose_name


##class Int(models.Model):
##    unique_id_a = models.IntegerField()
##    unique_id_b = models.IntegerField()
##    alias_a = models.TextField()
##    alias_b = models.TextField()
##    experimental_system_type = models.CharField(max_length=48, blank=True)
##    interaction_type = models.TextField(blank=True)
##    experimental_system = models.TextField(blank=True)
##    modification = models.CharField(max_length=61, blank=True)
##    taxid_a = models.IntegerField()
##    taxid_a = models.IntegerField()
##    pmid = models.TextField(blank=True)
##    source_database = models.CharField(max_length=95)
##    score = models.IntegerField()

#http://stackoverflow.com/questions/10143614/saving-nested-models-in-django-norel-gives-cant-encode-error
##from djnagotoolbox.fields import SetField, ListField, EmbeddedModelField
##
##
##class Graph(models.Model):
##    links = ListField(EmbeddedModelField('Link'))
##
##
##class Link(models.Model):
##    parent = EmbeddedModelField('Node')
##    child = EmbedddModelField('Node')
##
##
##class Node(models.Model):
##    extent = SetField() # Set of strings e.g. "Gene-Bmp4"
##    intent = SetField() # Set of strings.


if __name__ == '__main__':
    n1 = Node(extent=["Gene-bmp4"], intent=["Attr1", "Attr2"])
    n2 = Node(extent=["Gene-fbp4"], intent=["Attr3", "Attr4"])
    link = Link(parent=n1, child=n2)
    links = [link]
    g = Graph(links=links)
    g.save()
        
