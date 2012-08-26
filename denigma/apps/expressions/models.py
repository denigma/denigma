from django.db import models


class YeastDR(models.Model):
    exp = models.FloatField()
    ctr = models.FloatField()
    fold_change = models.FloatField()
    gene_symbol = models.CharField(max_length=30, blank=True)
    ensembl_gene = models.CharField(max_length=9)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    name = 'wtcrvsyepd1'

    def __unicode(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Yeast DR" # -differential expressed gene
        verbose_name_plural = verbose_name

    
class Lin2002(models.Model):
    orf = models.CharField(max_length=9)
    description = models.CharField(max_length=223, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    hap4oe1 = models.FloatField(null=True, blank=True)
    hap4oe2 = models.FloatField(null=True, blank=True)
    hxk2 = models.FloatField(null=True, blank=True)
    low_glucose1 = models.FloatField(null=True, blank=True)
    low_glucose2 = models.FloatField(null=True, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    name = 'Lin2002'

    def __unicode(self):
        return gene_symbol

    class Meta:
       verbose_name = "DR, hxk2 and HAP4OE"
       verbose_name_plural = verbose_name

class sip2delta_aging(models.Model):
    orf = models.CharField(max_length=11)
    gene_symbol = models.CharField(max_length=5, blank=True)
    fold_change = models.FloatField()
    description = models.CharField(max_length=172)
    main_process = models.CharField(max_length=56)
    specific_process = models.CharField(max_length=29, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    strain = 'YB614'
    concentration = 'sip2'
    incubation = 'age'
    name = 'sip2_aging'

    def __unicode(self):
        return gene_symbol

    class Meta:
        verbose_name = "SIP2delta aging" #  differential expressed gene
        verbose_name_plural = verbose_name

class sip2delta_wt(models.Model):
    orf = models.CharField(max_length=11)
    gene_symbol = models.CharField(max_length=6, blank=True)
    fold_change = models.FloatField()
    description = models.CharField(max_length=178)
    main_process = models.CharField(max_length=56)
    specific_process = models.CharField(max_length=38, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    strain = 'YB614/YB332'
    concentration = 'sip2'
    incubation = 'wt'
    name = 'sip2_wt'

    def __unicode(self):
        return gene_symbol

    class Meta:
        verbose_name = "SIP2delta" # differential expressed gene
        verbose_name_plural = verbose_name

class snf4delta_aging(models.Model):
    orf = models.CharField(max_length=11)
    gene_symbol = models.CharField(max_length=7, blank=True)
    fold_change = models.FloatField()
    description = models.CharField(max_length=155)
    main_process = models.CharField(max_length=56)
    specific_process = models.CharField(max_length=29, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    name = 'snf4_aging'
    strain = 'YB614'
    concentration = 'snf4'
    incubation = 'age'

    def __unicode(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "SNF4delta aging" #  differential expressed gene
        verbose_name_plural = verbose_name

class snf4delta_wt(models.Model):
    orf = models.CharField(max_length=11)
    gene_symbol = models.CharField(max_length=6, blank=True)
    fold_change = models.FloatField()
    description = models.CharField(max_length=127)
    main_process = models.CharField(max_length=56)
    specific_process = models.CharField(max_length=32, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    strain = 'YB614/YB332'
    concentration = 'snf4'
    incubation = 'wt'
    name = 'snf4_wt'

    def __unicode(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "SNF4delta" # differential expressed gene
        verbose_name_plural = verbose_name

class wt_aging(models.Model):
    orf = models.CharField(max_length=11)
    gene_symbol = models.CharField(max_length=6, blank=True)
    fold_change = models.FloatField()
    description = models.CharField(max_length=146)
    main_process = models.CharField(max_length=56)
    specific_process = models.CharField(max_length=54, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    strain = 'YB332'
    concentration = ''
    incubation = 'age'
    name = 'wt_aging'

    def __repr__(self):
        return self.gene_symbol

    def __str__(self):
        return "{0} {1} {2}".format(self.orf, self.gene_symbol, self.fold_change)

    class Meta:
        verbose_name = "Yeast aging" #  differential expressed gene
        verbose_name_plural = verbose_name


class Rapamycin(models.Model):
    orf = models.CharField(max_length=9)
    rapamycin_replicate_1 = models.FloatField()
    rapamycin_replicate_2 = models.FloatField()
    rapamycin_mean = models.FloatField(blank=True)
    fpr1_8_rapamycin_replicate_1 = models.FloatField(blank=True)
    fpr1_8_rapamycin_replicate_2 = models.FloatField()
    fpr1_8_rapamycin_replicate_3 = models.FloatField()
    fpr1_8_rapamycin_mean = models.FloatField()
    ly_83583_replicate_1 = models.FloatField()
    ly_83583_replicate_2 = models.FloatField()
    ly_83583_mean = models.FloatField(blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    fold_change = models.FloatField()

    def __unicode__(self):
       return self.orf

    class Meta:
        verbose_name = "rapamycin differential expressed gene"
    
class rapamycin_protein(models.Model):
    protein = models.CharField(max_length=9)
    fold_change = models.FloatField()
    protein_function = models.CharField(max_length=82)
    taxid = 4932
    pmid = 18270585
    orf = models.CharField(max_length=9)
    gene_symbol = models.CharField(max_length=10, blank=True)
    strain = 'BJ5465'
    concentration = '200 nM'
    incubation = 'Rapamycin 70 min'

    def __unicode__(self):
        return self.protein

    class Meta:
        verbose_name = "rapamycin differential expressed protein"


class AgeMap(models.Model):
    unigene = models.CharField(max_length=9)
    gene_symbol = models.CharField(max_length=13, blank=True)
    gene_ontology = models.TextField(blank=True)
    adrenals_age_coef = models.FloatField()
    cerebellum_age_coef = models.FloatField()
    eye_age_coef = models.FloatField()
    gonads_age_coef = models.FloatField()
    heart_age_coef = models.FloatField()
    lung_age_coef = models.FloatField()
    spleen_age_coef = models.FloatField()
    spinal_cord_age_coef = models.FloatField()
    thymus_age_coef = models.FloatField()
    empirical_meta_analysis_value = models.FloatField()
    empirical_meta_analysis_p_value = models.FloatField()
    classification = models.CharField(max_length=5)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 10090

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "AGEMAP"
        verbose_name_plural = verbose_name


class AgingSignature(models.Model):
    mapping = models.IntegerField(null=True, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    gene_name = models.CharField(max_length=93, blank=True)
    gene_symbol = models.CharField(max_length=20, blank=True)
    human_brain = models.CharField(max_length=8, blank=True)
    human_kidney = models.CharField(max_length=8, blank=True)
    human_muscle_1 = models.CharField(max_length=8, blank=True)
    human_muscle_2 = models.CharField(max_length=8, blank=True)
    mouse_brain = models.CharField(max_length=8, blank=True)
    mouse_cochlea = models.CharField(max_length=8, blank=True)
    mouse_eye = models.CharField(max_length=8, blank=True)
    mouse_heart = models.CharField(max_length=8, blank=True)
    mouse_hematopoietic = models.CharField(max_length=8, blank=True)
    mouse_hippocampus = models.CharField(max_length=8, blank=True)
    mouse_kidney = models.CharField(max_length=8, blank=True)
    mouse_liver = models.CharField(max_length=8, blank=True)
    mouse_lung = models.CharField(max_length=8, blank=True)
    mouse_muscle = models.CharField(max_length=8, blank=True)
    mouse_myoblast = models.CharField(max_length=8, blank=True)
    mouse_neocortex = models.CharField(max_length=8, blank=True)
    rat_cardiac = models.CharField(max_length=8, blank=True)
    rat_extraocular = models.CharField(max_length=8, blank=True)
    rat_glia = models.CharField(max_length=8, blank=True)
    rat_hippocampal_ca1_1 = models.CharField(max_length=8, blank=True)
    rat_hippocampal_ca1_2 = models.CharField(max_length=8, blank=True)
    rat_hippocampus = models.CharField(max_length=8, blank=True)
    rat_larynge = models.CharField(max_length=8, blank=True)
    rat_muscle = models.CharField(max_length=8, blank=True)
    rat_oculomotor = models.CharField(max_length=8, blank=True)
    rat_spinal = models.CharField(max_length=8, blank=True)
    rat_stromal = models.CharField(max_length=8, blank=True)
    n_genes = models.IntegerField()
    n_overexpressed = models.IntegerField()
    n_underexpressed = models.IntegerField()
    p_value = models.FloatField()
    q_value = models.FloatField()
    taxid = models.IntegerField(null=True, blank=True)
    classification = models.CharField(max_length=8)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Aging signature"
        verbose_name_plural = "Aging signature"


class AgingSignatureChi(models.Model):
    mapping = models.IntegerField(null=True, blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    gene_name = models.CharField(max_length=89, blank=True)
    gene_symbol = models.CharField(max_length=20, blank=True)
    human_brain = models.FloatField()
    human_kidney = models.FloatField()
    human_muscle_1 = models.FloatField()
    human_muscle_2 = models.FloatField()
    mouse_brain = models.FloatField()
    mouse_cochlea = models.FloatField()
    mouse_eye = models.FloatField()
    mouse_heart = models.FloatField()
    mouse_hematopoietic = models.FloatField()
    mouse_hippocampus = models.FloatField()
    mouse_kidney = models.FloatField()
    mouse_liver = models.FloatField()
    mouse_lung = models.FloatField()
    mouse_muscle = models.FloatField()
    mouse_myoblast = models.FloatField()
    mouse_neocortex = models.FloatField()
    rat_cardiac = models.FloatField()
    rat_extraocular = models.FloatField()
    rat_glia = models.FloatField()
    rat_hippocampal_ca1_1 = models.FloatField()
    rat_hippocampal_ca1_2 = models.FloatField()
    rat_hippocampus = models.FloatField()
    rat_larynge = models.FloatField()
    rat_muscle = models.FloatField()
    rat_oculomotor = models.FloatField()
    rat_spinal = models.FloatField()
    rat_stromal = models.FloatField()
    n_genes = models.IntegerField()
    p_value = models.FloatField()
    taxid = models.IntegerField()
    classification = models.CharField(max_length=5)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Aging signature (chi)"
        verbose_name_plural = "Aging signature (chi)"


class AgingLui2010(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=13)
    observation = models.CharField(max_length=95)
    pubmedid = models.IntegerField()
    reference = models.CharField(max_length=16)
    classification = models.CharField(max_length=5)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Aging gene expression changes originating from juvenile growth"
        verbose_name_plural = "Aging gene expression changes originating from juvenile growth"


class AgingTranscriptome(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    unigene_id = models.CharField(max_length=9)
    gene_name = models.CharField(max_length=162)
    gene_symbol = models.CharField(max_length=13, blank=True)
    chromosome = models.IntegerField()
    rna_nucleotide_accession_version = models.CharField(max_length=219, blank=True)
    changes_in_aging = models.CharField(max_length=13)
    classification = models.CharField(max_length=5)
    taxid = 10090
    pocessing = '''
    Primary mapping against Entre gene symbols yielded 410 of 478 mapping, while 6 were mapped to multiple and 62 weren't mapped.
    Secondary mapping was performed against alias Alias, full_name_from_nomenclature_autority EntrezGene and rna_nucleotide_accession_version RnaNucleotideAccessionVersion.
    This resulted in 9 remaining unmapped ids and 9 mapped to multiple.
    Note, there are multiple rna_nucleotide_accession_version present for some genes.
    Mapping remaining unmapped Ids manually.
    
    unigene_id = 'Mm.358622' --> entrez_gene_id = 235043 chromosome = 9
    gene_symbol = 'LOC626578' --> entrez_gene_id = 626578
    rna_nucleotide_accession_version = 'XM_987614 XM_987759 XM_987820 XM_987793 XM_987647 XM_987723 XM_987560 XM_987685 XM_987589 NM_008620 NM_001039646 XM_987524'
    --> (This sequence has been replaced by) rna_nucleotide_accession_version = 'NM_001039646' --> entrez_gene_id = 626578
    chromosome = 5
    
    unigene_id = 'Mm.253329' --> entrez_gene_id = 235043 chromosome = 9
    gene_symbol = 'BC010787' --> entrez_gene_id = 235043 chromosome = 9
    rna_nucleotide_accession_version = NM_178577 --> entrez_gene_id = 235043


    retired unigene_id --> Mm.392548 --> NP_862900.1 -- entrez_gene_id = 107849 chromosome = 13
    rna_nucleotide_accession_version = 'NM_011954 NM_011118 NM_031191' --> entrez_gene_id = 26421

    Mm.1458 --> entrez_gene_id = 19062 chromosome 11
    gene_symbol = 'RP23-136K12.4' --> locus_tag =  'RP23-136K12.4' --> entrez_gene_id = 19062 chromosome 11
    rna_nucleotide_accession_version = NM_008916 --> entrez_gene_id = 19062 chromosome 11

    Mm.379292 --> entrez_gene_id = 108946 chromosome = 3
    LOC668898 --> entrez_gene_id = 668898 chromosome = 3
    XM_001004501 --> entrez_gene_id = 668898 chromosome = 3
    This gene mapping is difficult. As the latter id appear to be withdraw and its location is the some as the former. the former Zzz3 will be selected.

    entrez_gene_id = 107849 chromosome 13
    The same as entrez_gene_id = 26421, above! Double entry!

    Mm.42040 --> entrez_gene_id = 11639 chromosome = 4
    gene_name = 'Adenylate kinase 3 alpha-like 1'
    --> entrez_gene_id = 56248 chromosome = 19
    --> entrez_gene_id = 11639 chromosome = 4
    NM_009647 --> entrez_gene_id = 11639

    Mm.292803 --> entrez_gene_id = 104158 chromosome = 8
    NM_053200 --> entrez_gene_id = 104158 chromosome = 8

    Mm.381765 --> retired unigene_id --> entrez_gene_id = 80750 chromosome  = 8
    XM_894155 --> This sequence has been replaced by NM_030563. --> entrez_gene_id = 80750
    BC004022 --> entrez_gene_id = 80750
    '''

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Aging transcriptome"

    
class Cc3(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_cc_f = models.FloatField()
    anova_cc_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_cc = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=10)
    locus_tag = models.CharField(max_length=10)
    ws195_wormbase_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    cycling = models.CharField(max_length=54)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light and temperature exntrained constant cold (3-day)"
        verbose_name_plural = verbose_name


class Cd(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=18)
    scn = models.FloatField(null=True, blank=True)
    liv = models.FloatField(null=True, blank=True)
    kid = models.FloatField(null=True, blank=True)
    aor = models.FloatField(null=True, blank=True)
    skm = models.FloatField(null=True, blank=True)
    hat = models.FloatField(null=True, blank=True)
    adg = models.FloatField(null=True, blank=True)
    bat = models.FloatField(null=True, blank=True)
    wat = models.FloatField(null=True, blank=True)
    bon = models.FloatField(null=True, blank=True)
    pfr = models.FloatField(null=True, blank=True)
    wb = models.FloatField(null=True, blank=True)
    atr = models.FloatField(null=True, blank=True)
    ven = models.FloatField(null=True, blank=True)
    num_tissue = models.IntegerField()
    range_p = models.FloatField()
    peak_mean = models.FloatField()
    taxid = 10090
    classification = 'CD'
    processing = '''
    This dataset only provided gene symbols.
    First mapping were performed directly against EntrezGene gene_symbol.
    As a result out of total 9955, 8728 were mapped (1), 1218 results couldn't been mapped (0) and 9 mapped multiple ids (2).
    The unmapped Ids number is to high for manually mapping and there are no other information as gene symbols.
    Second mapping will be performed against Alias alias. Mapping11.py
    It could be intersting to map also the already mapped ids against Alias alias in order to identify genes which were mapped uncorrectly to the wrong gene_symbol in EntrezGene.
    Or using different source data from Ensembl, Uniprot, MGI.
    
    14.0.2011 Converted Disconected Ids to current_entrez_gene_ids via mapping10.py:
    Changed Gene Hsp110 in Dataset Cd from 15506 to 15525
    Changed Gene Hnrpa2b1 in Dataset Cd from 15383 to 53379
    Changed Gene Ela1 in Dataset Cd from 13704 to 109901
    Changed Gene Cdc2l1 in Dataset Cd from 12536 to 12537
    Changed Gene Gprc2a-rs1 in Dataset Cd from 12375 to 110931
    Changed Gene Gpt1 in Dataset Cd from 14774 to 76282
    Changed Gene Gt4-1 in Dataset Cd from 14877 to 239719
    Changed Gene Gtl2 in Dataset Cd from 14893 to 17263
    Changed Gene H2-T17 in Dataset Cd from 15032 to 15039
    Changed Gene Igk-V19-14 in Dataset Cd from 16092 to 667881
    Changed Gene Mem1 in Dataset Cd from 17280 to 382620
    '''

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "constant darkness ciracdian gene"


class CrSignature(models.Model):
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=13)
    gene_name = models.CharField(max_length=99)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    total = models.IntegerField()
    overexp = models.IntegerField()
    underexp = models.IntegerField()
    p_value = models.FloatField()
    classification = models.CharField(max_length=5)
    taxid = 10090

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "DR-signature"
        verbose_name_plural = "DR-signature"
    

class CrTranscriptome(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    unigene_id = models.CharField(max_length=9)
    gene_name = models.CharField(max_length=128)
    gene_symbol = models.CharField(max_length=13, blank=True)
    chromosome = models.IntegerField()
    rna_nucleotide_accession_version = models.CharField(max_length=155, blank=True)
    changes_in_cr = models.CharField(max_length=13)
    classification = models.CharField(max_length=5)
    taxid = 10090
    processing = '''
    14.0.2011 Converted Disconected Ids to current_entrez_gene_ids via mapping10.py:
    Changed Gene Hsp110 in Dataset CrTranscriptome from 15506 to 15525
    
    Primary mapping against Entre gene symbols yielded 519 of 586 total mappings, while 13 were mapped to multiple and  54  weren't mapped.
    Secondary mapping was performed against alias Alias, full_name_from_nomenclature_autority EntrezGene and rna_nucleotide_accession_version RnaNucleotideAccessionVersion.
    This resulted in 5 remaining unmapped ids and 14 mapped to multiple.
    Note, there are multiple rna_nucleotide_accession_version present for some genes.
    Mapping remaining unmapped Ids manually.

    Mm.292803 --> entrez_gene_id = 104158 chromosome = 8
    NM_053200 --> entrez_gene_id = 104158 chromosome = 8
    
    Mm.148155 --> entrez_gene_id = 17436 chromosome = 9
    gene_name = 'Malic enzyme, supernatant' -->  entrez_gene_id = 17436
    NM_008615 -->  entrez_gene_id = 17436

    Mm.1458 --> entrez_gene_id = 19062 chromosome 11
    gene_symbol = 'RP23-136K12.4' --> locus_tag =  'RP23-136K12.4' --> entrez_gene_id = 19062 chromosome 11
    rna_nucleotide_accession_version = NM_008916 --> entrez_gene_id = 19062 chromosome 11

    Mm.343110 --> entrez_gene_id = 14433 chromosome = 6
    AK190093 --> entrez_gene_id = 14433
    NM_001001978 NM_001001303 NM_008084 -->  entrez_gene_id = 14433 chromosome = 6
    This gene is located on the wrong chromosme as given and it is known as houskeeping gene.

    Mm.290589 retired unigene_id --> entrez_gene_id = 13216 chromomsome = 8
    NM_010031 --> entrez_gene_id = 13216 chromomsome = 8
    NM_001012307 --> entrez_gene_id = 497114 chromomsome = 8
    Difficult gene mapping, chose the former one as it was mapped two times. Actually there is no reason

    Of the ids mapped to multiple entrez gene ids the followiing were manually corrected:
    Ak3 was accendidalt mapped to entrez_gene_id 11639 (via alias Alias?)
    Mm.196067 --> entrez_gene_id = 56248 chromosome = 19
    NM_021299 --> entrez_gene_id = 56248 chromosome = 19
    '''
    taxid = 10090

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = "DR-transcriptome"


class Dd(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_set = models.CharField(max_length=11)
    anova_f_stat = models.FloatField()
    anova_pvalue = models.FloatField()
    gene_symbol = models.CharField(max_length=15)
    ct_number = models.CharField(max_length=8, blank=True)
    genbank_accession_number = models.CharField(max_length=8, blank=True)
    ensembl_gene_id = models.CharField(max_length=12)
    taxid = 7227
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = "Light and temperature entrained constant darkness (3-day)"
       verbose_name_plural = verbose_name


class Dd3(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_f = models.FloatField()
    anova_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_dd = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=10)
    locus_tag = models.CharField(max_length=11)
    ws195_wormbase_gene_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    cycling = models.CharField(max_length=54)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light and temperature entrained constant darkness (3-day)"
        verbose_name_plural = verbose_name


class FastingInducedGenes(models.Model):
    gene_symbol = models.CharField(max_length=8, blank=True)
    ncbi_kogs = models.CharField(max_length=66, blank=True)
    locus_tag = models.CharField(max_length=10)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 6239
    classification = 'DD DI'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "fasting-induced gene"


class ImprintedGeneNetwork(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=8)
    lung_fold_change_1_to_4wk = models.FloatField(null=True, blank=True)
    lung_p_value_1_to_4wk = models.FloatField(null=True, blank=True)
    lung_fold_change_1_to_8wk = models.FloatField(null=True, blank=True)
    lung_p_value_1_to_8wk = models.FloatField(null=True, blank=True)
    kidney_fold_change_1_to_4wk = models.FloatField(null=True, blank=True)
    kidney_p_value_1_to_4wk = models.FloatField(null=True, blank=True)
    kidney_fold_change_1_to_8wk = models.FloatField(null=True, blank=True)
    kidney_p_value_1_to_8wk = models.FloatField(null=True, blank=True)
    heart_fold_change_1_to_4wk = models.FloatField(null=True, blank=True)
    heart_p_value_1_to_4wk = models.FloatField(null=True, blank=True)
    consistency = models.CharField(max_length=3)
    p_value = models.CharField(max_length=3, blank=True)
    fold_change_higher_as_5 = models.CharField(max_length=3, blank=True)
    classification = models.CharField(max_length=8)
    processing = '''
    14.0.2011 Converted Disconected Ids to current_entrez_gene_ids via mapping10.py:
    Changed Gene GTL2 in Dataset ImprintedGeneNetwork from 14893 to 17263
    '''
    taxid = 10090

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Imprinted aging differential expressed gene"


class JuvenileInduced(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    probe_set = models.CharField(max_length=12)
    gene_symbol = models.CharField(max_length=13)
    gene_name = models.CharField(max_length=94)
    heart = models.FloatField()
    kidney = models.FloatField()
    lung = models.FloatField()
    taxid = 10090
    classification = 'JI'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "juvenile-induced gene"


class JuvenileSuppressed(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    probe_set = models.CharField(max_length=12)
    gene_symbol = models.CharField(max_length=15)
    gene_name = models.CharField(max_length=99)
    heart = models.CharField(max_length=5)
    kidney = models.FloatField()
    lung = models.FloatField()
    taxid = 10090
    classification = 'JS'
    procession = '''
    Initially mapping  of gene_symbols, gene_names couldn't map for 5 (0) of 41 total.
    As gene_symbols gene_names are present as well as additional ids manually curation of this 5 were performed.

    gene_symbol = 'Rkhd3'; gene_name = 'ring finger and KH domain containing 3'; probe_set = '1437152_at'
    entrez_gene_id = 108797; gene_symbol = 'Mex3b'; alias = ['Rkhd3']

    gene_symbol = '4833427B12Rik'; gene_name = 'RIKEN cDNA 4833427B12 gene'; probe_set_id = '1428713_s_at'
    discontinued_id = 73769; entrez_gene_id = 272551; gene_symbol = 'Gins2'; gene_name = 'GINS complex subunit 2 (Psf2 homolog)'

    gene_symbol = 'Sox4' OR 'LOC672274'; gene_name = 'SRY-box containing gene 4'; probe_set = '1419157_at'
    gene_symbol = 'Sox4'; discondinued_id = 672274; entrez_gene_id = 20677
    
    gene_symbol = 'LOC632764'; gene_name = 'Transcribed locus, weakly similar to XP_484135.1 PREDICTED: hypothetical protein XP_484135 [Mus mus'; probe_set = '1455038_at'
    gene_symbol = '5730471H19Rik'; gene_name = 'RIKEN cDNA 5730471H19 gene'; entrez_gene_id = 632764

    gene_symbol = '2600005O03Rik'; gene_name = 'RIKEN cDNA 2600005O03 gene', probe_set = '1452912_at'
    gene_symbol = 'Dscc1'; gene_name = ' defective in sister chromatid cohesion 1 homolog (S. cerevisiae)' entrez_gene_id = 72107 
    '''

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "juvenile-suppressed gene"


class Ld(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_set = models.CharField(max_length=11)
    anova_f_stat = models.FloatField()
    anova_pvalue = models.FloatField()
    gene_symbol = models.CharField(max_length=34)
    ct_number = models.CharField(max_length=8, blank=True)
    genbank_accession_number = models.CharField(max_length=8)
    ensembl_gene_id = models.CharField(max_length=12)
    taxid = 7227
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light/dark cycling circadian gene"


class Ld3(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_f = models.FloatField()
    anova_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_ld = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=10)
    locus_tag = models.CharField(max_length=10)
    ws195_wormbase_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=25, blank=True)
    cycling = models.CharField(max_length=54)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light and temperature driven light/dark (day-3)"
        verbose_name_plural = verbose_name


class Lddd6(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_dd_f = models.FloatField()
    anova_dd_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_ld = models.FloatField()
    fold_change_dd = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=10)
    locus_tag = models.CharField(max_length=10)
    ws195_wormbase_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    cycling = models.CharField(max_length=52)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
         verbose_name = "Light and Temperature entrained light/dark and constant darkness"
         verbose_name_plural = verbose_name


class PostnatalGeneticProgram(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=13)
    fold_change_from_1_to_4_wk_mouse_heart = models.FloatField()
    p_value_1_vs_4_wk_mouse_heart = models.FloatField()
    fold_change_from_1_to_4_wk_mouse_kidney = models.FloatField()
    p_value_1_vs_4_wk_mouse_kidney = models.FloatField()
    fold_change_from_1_to_8_wk_mouse_kidney = models.FloatField()
    p_value_1_vs_8_wk_mouse_kidney = models.FloatField()
    fold_change_from_1_to_4_wk_mouse_lung = models.FloatField()
    p_value_1_vs_4_wk_mouse_lung = models.FloatField()
    fold_change_from_1_to_8_wk_mouse_lung = models.FloatField()
    p_value_1_vs_8_wk_mouse_lung = models.FloatField()
    fold_change_from_1_to_5_wk_rat_lung = models.FloatField()
    p_value_1_vs_5_wk_rat_lung = models.FloatField()
    fold_change_from_1_to_5_wk_rat_kidney = models.FloatField()
    p_value_1_vs_5_wk_rat_kidney = models.FloatField()
    classification = models.CharField(max_length=5)
    taxid = 10090

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        db_table = u'postnatal_genetic_program'
        verbose_name = "postnatal genetic program"
        verbose_name_plural = "postnatal genetic program"


class Swindell2009(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=18)
    observation = models.CharField(max_length=172, blank=True)
    pubmed_id = models.IntegerField()
    reference = models.CharField(max_length=14, blank=True)
    classification = models.CharField(max_length=5)
    p_value = models.FloatField()
    ensembl_gene_id = models.CharField(max_length=18, blank=True)
    taxid = 10090
    processing = '''
    14.01.2011 Converted Disconected Ids to current_entrez_gene_ids via mapping10.py:
    Changed Gene Ela1 in Dataset Swindell2009 from 13704 to 109901

    Primary Mapping ageing EntrezGene yielded 846 mappings of 900, 52 gene_symbols couldn't be mapped.
    
    23.01.2011 Transfered 900 DD from Gendr to this table via Corrector.py.
    Secondary mapping with mapping17.py
    17 of 1800 were not mapped. Starting manually mapping.
    Couldn't find anything for Mm.466684 
    100042889 - Entrez gene Id?
    Mm.462196 Nope

    gene_symbol = 'Sfrs10' --> entrez_gene_id = 20381; disconnected and replaced with entrez_gene_id = 20382
    Tra2b is also known as Sfrs10, but as Sfrs2 has Sfrs10 as a gene_symbol of a disconnected id, it will be chosen.

    Mm.392176 is entrez_gene_id = 18616, Chromosome = 7

    Mm.393717 nothing

    Mm.34106 --> gene_symbol = 'Zbtb16', entrez_gene_id = 235320; chromosome = 9

    1200016E24Rik --> disconected entrez_gene_id = 319202

    LOC100047628 --> disconected entrez_gene_id = 100047628

    LOC100043766 --> entrz_gene_id = 100043766

    Sfrs10--> entrez_gene_id = 20381; disconnected and replaced with entrez_gene_id = 20382
    Tra2b is also known as Sfrs10, but as Sfrs2 has Sfrs10 as a gene_symbol of a disconnected id, it will be chosen.

    BC033915 --> entrez_gene_id = 70661

    LOC100044979 --> disconected entrez_gene_d = 100044979

    Mm.440242 --> nothing

    LOC100048085 --> disconected entrez_gene_id = 100048085
    similar to ectonucleoside triphosphate diphosphohydrolase 4
    it could be "Entpd4" --> entrez_gene_id = 67464
        
    '''

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "CR-signature"
        verbose_name_plural = "CR-signature"


class Wc5(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_f = models.FloatField()
    anova_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_wc = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=11)
    locus_tag = models.CharField(max_length=11)
    ws195_wormbase_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    cycling = models.CharField(max_length=54)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light and temperature driven warm/cold cycling (day-5)"
        verbose_name_plural = verbose_name


class Wccc6(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    affymetrix_probe_id_set = models.CharField(max_length=11)
    fourier_f24 = models.FloatField()
    fourier_pvalue = models.FloatField()
    anova_cc_f = models.FloatField()
    anova_cc_pvalue = models.FloatField()
    phase = models.FloatField()
    ac24_avg = models.FloatField()
    ac24_max = models.FloatField()
    fold_change_wc = models.FloatField()
    fold_change_cc = models.FloatField()
    expression_avg = models.FloatField()
    gene_symbol = models.CharField(max_length=10)
    locus_tag = models.CharField(max_length=10)
    ws195_wormbase_goterm_info = models.TextField(blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    cycling = models.CharField(max_length=52)
    taxid = 6239
    classification = 'CD'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "Light and temperature entrained warm/cold and constant cold"
        verbose_name_plural = verbose_name


class miRNA_MSC_all(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    identifier = models.IntegerField()
    gene_symbol = models.CharField(max_length=17)
    aveexpr = models.FloatField()
    t = models.FloatField()
    p_value = models.FloatField()
    adj_p_val = models.FloatField()
    b = models.FloatField()
    taxid = 9606

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "MSC miRNA "
        verbose_name_plural = "MSC miRNA"


class miRNA_MSC_young(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    identifier = models.IntegerField()
    gene_symbol = models.CharField(max_length=32)
    aveexpr = models.FloatField()
    t = models.FloatField()
    p_value = models.FloatField()
    adj_p_val = models.FloatField()
    b = models.FloatField()
    taxid = 9606

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "MSC young miRNA"
        verbose_name_plural = "MSC young miRNA"


class miRNA_young_old(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    identifier = models.IntegerField()
    gene_symbol = models.CharField(max_length=32)
    aveexpr = models.FloatField()
    t = models.FloatField()
    p_value = models.FloatField()
    adj_p_val = models.FloatField()
    b = models.FloatField()
    taxid = 9606

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "MSC young vs. old miRNA"
        verbose_name_plural = "MSC young vs. old miRNA"


class WormDR(models.Model):
    probe_id = models.CharField(max_length=25)
    entrez_gene = models.CharField(max_length=24, blank=True)
    gene_symbol = models.CharField(max_length=40, blank=True)
    gene_name = models.CharField(max_length=224, blank=True)
    exp = models.FloatField()
    ctr = models.FloatField()
    fold_change = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "nematode DR-differential expressed gene"


class S288c_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "9 mM"
    incubation = "Caffeine 30 min"
    strain =  "S288c"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 9 mM caffeine (S288c)"
        verbose_name_plural = "yeast 9 mM caffeine (S288c)"


class S288c_rapamycin(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "200 ng/mL"
    incubation = "Rapamycin 30 min"
    strain = "S288c"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 200 ng/mL rapamycin 30 min (S288c)"
        verbose_name_plural = "yeast 200 ng/mL rapamycin 30 min (S288c)"


class Sigma2000_rapamycin(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "200 ng/mL"
    incubation = "Rapamycin 30 min"
    strain =  "Sigma 2000"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 200 ng/mL rapamcyin 30 min (Sigma 2000)"
        verbose_name_plural = "yeast 200 ng/mL rapamycin 30 min (Sigma 2000)"


class Sigma2000_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "9 mM"
    incubation = "Caffeine 30 min"
    strain =  "Sigma 2000"

    def __unicode__(self):
       return self.gene_symbol    

    class Meta:
        verbose_name = "yeast 9 mM caffeine 30 min (Sigma 2000)"
        verbose_name_plural = "yeast 9 mM caffeine 30 min (Sigma 2000)"


class W303a_0p3mM_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "0.3 mM"
    incubation = "Caffeine 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 0.3 mM caffeine 30 min (W303a)"
        verbose_name_plural = "yeast 0.3 mM caffeine 30 min (W303a)"


class W303a_1mM_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=9, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "1 mM"
    incubation = "Caffeine 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 1 mM caffeine 30 min (W303a)"
        verbose_name_plural = "yeast 1 mM caffeine 30 min (W303a)"


class W303a_1ng_mL_rapamycin(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "1 ng/mL"
    incubation = "Rapamycin 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 1 ng/mL rapamycin 30 min (W303a)"
        verbose_name_plural = "yeast 1 ng/mL rapamycin 30 min (W303a)"


class W303a_200ng_mL_rapamycin(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "200 ng/mL"
    incubation = "Rapamycin 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 200 ng/mL rapamycin 30 min (W303a)"
        verbose_name_plural = "yeast 200 ng/mL rapamcyin 30 min (W303a)"


class W303a_3mM_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "3 mM"
    incubation = "Caffeine 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 3 mM caffeine 30 min (W303a)"
        verbose_name_plural = "yeast 3 mM caffeine 30 min (W303a)"


class W303a_5ng_mL_rapamycin(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=9, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "5 ng/mL"
    incubation = "Rapamycin 30 min"
    strain =  "W303a"

    def __unicode__(self):
       return self.gene_symbol

    class Meta:
         verbose_name = "yeast 5 ng/mL rapamycin 30 min (W303a)"
         verbose_name_plural = "yeast 5 ng/mL rapamycin 30 min (W303a)"


class W303a_6mM_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "6 mM"
    incubation = "Caffeine 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
         verbose_name = "yeast 6 mM caffeine 30 min (W303a)"
         verbose_name_plural = "yeast 6 mM caffeine 30 min (W303a)"


class W303a_9mM_caffeine(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "9 mM"
    incubation = "Caffeine 30 min"
    strain =  "W303a"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 9 mM caffeine 30 min (W303a)"
        verbose_name_plural = "yeast 9 mM caffeine 30 min (W303a)"


class BY4741_rapamycin_200ng_mL_1h(models.Model):
    probe_id = models.CharField(max_length=10)
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.CharField(max_length=144, blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=10)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.CharField(max_length=176, blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "200 ng/mL"
    incubation = "Rapamycin 60 min"
    strain =  "BY4741"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "yeast 200 ng/mL rapamycin 60 min (BY4741)"
        verbose_name_plural = "yeast 200 ng/mL rapamycin 60 min (BY4741)"


class BY4741_rapamycin_30min(models.Model):
    probe_id = models.CharField(max_length=12)
    unigene_title = models.CharField(max_length=1, blank=True)
    nucleotide_title = models.CharField(max_length=1, blank=True)
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)
    go_component_id = models.TextField(blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=9)
    platform_cloneid = models.CharField(max_length=1, blank=True)
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)
    unigene_symbol = models.CharField(max_length=1, blank=True)
    platform_spotid = models.CharField(max_length=1, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)
    fold_change = models.FloatField()
    concentration = "? ng/mL"
    incubation = "Rapamycin 30 min"
    strain =  "BY4741"

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = "yeast rapamcyin 30 min (BY4741)"
       verbose_name_plural = "yeast rapamycin 30 min (BY4741)"
     

class FlyDR_trn(models.Model):
    probe_id = models.CharField(max_length=23)
    entrez_gene = models.CharField(max_length=37, blank=True)
    gene_symbol = models.CharField(max_length=46, blank=True)
    gene_name = models.CharField(max_length=97, blank=True)
    ensembl_gene = models.CharField(max_length=11, blank=True)
    exp = models.FloatField()
    ctr = models.FloatField()
    fold_change = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "fruit fly DR-translational" # differential expressed gene
        verbose_name_plural = verbose_name


class FlyDR_10day(models.Model):
    probe_id = models.CharField(max_length=25)
    entrez_gene = models.CharField(max_length=37, blank=True)
    gene_symbol = models.CharField(max_length=46, blank=True)
    gene_name = models.CharField(max_length=97, blank=True)
    ensembl_gene = models.CharField(max_length=11, blank=True)
    exp = models.FloatField()
    ctr = models.FloatField()
    fold_change = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "fruit fly DR-transcriptional (10 days)" # differential expressed gene
        verbose_name_plural = verbose_name


class FlyDR_40day(models.Model):
    probe_id = models.CharField(max_length=25)
    entrez_gene = models.CharField(max_length=37, blank=True)
    gene_symbol = models.CharField(max_length=46, blank=True)
    gene_name = models.CharField(max_length=97, blank=True)
    ensembl_gene = models.CharField(max_length=11, blank=True)
    exp = models.FloatField()
    ctr = models.FloatField()
    fold_change = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
       return self.gene_symbol

    class Meta:
       verbose_name = "fruit fly DR-transcriptional (40 days)" #  differential expressed genes 
       verbose_name_plural = verbose_name


class Spermidine(models.Model):
    probe_id = models.CharField(max_length=20, primary_key=True)
    unigene_title = models.CharField(max_length=1, blank=True)  #Delete, its empty
    nucleotide_title = models.CharField(max_length=1, blank=True)  #Delete, its empty
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True)  #Delete, its empty
    go_component_id = models.CharField(max_length=192, blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    ensembl_gene = models.CharField(max_length=11, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True)  #Delete, its empty
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)  #Delete, its empty
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)  #Delete, its empty
    unigene_symbol = models.CharField(max_length=1, blank=True)  #Delete, its empty
    platform_spotid = models.CharField(max_length=14, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)  #Delete, its empty
    fold_change = models.FloatField()

    def __unicode__(self):
        return self.gene_symbol
   
    class Meta:
        verbose_name = "spermidine differential expressed gene" 


class PI3K_m_vs_hx(models.Model):
    ensembl_id = models.CharField(max_length=23, blank=True)
    special = models.FloatField(blank=True)
    hx546_1 = models.IntegerField()
    m333_1 = models.IntegerField()
    hx546_2 = models.IntegerField()
    m333_2 = models.IntegerField()
    hx546_3 = models.IntegerField()
    m333_3 = models.IntegerField()
    hx546_4 = models.IntegerField()
    mg44_4 = models.IntegerField()
    hx546_5 = models.IntegerField()
    mg44_5 = models.IntegerField()
    hx546_6 = models.IntegerField()
    mg44_6 = models.IntegerField()
    hx546_7 = models.IntegerField()
    mg44_7 = models.IntegerField()
    hx546_8 = models.IntegerField()
    m333_8 = models.IntegerField()
    sum_m = models.IntegerField()
    sum_hx = models.IntegerField()
    sum_all = models.IntegerField()
    fold_change = models.FloatField(blank=True)
    log2 = models.FloatField(blank=True)
    expressed = models.BooleanField(blank=True)
    p_value = models.FloatField(blank=True)

    def __unicode__(self):
        return self.ensembl_id

    class Meta:
        verbose_name = "PI3K/age-1 m vs. hx"
        verbose_name_plural = verbose_name
 

class PI3K_m_vs_N2(models.Model):
    ensembl_id = models.CharField(max_length=23, blank=True)
    special = models.FloatField(blank=True)
    n2_1 = models.IntegerField()
    m333_1 = models.IntegerField()
    n2_2 = models.IntegerField()
    mg44_2 = models.IntegerField()
    n2_3 = models.IntegerField()
    mg44_3 = models.IntegerField()
    n2_4 = models.IntegerField()
    m333_4 = models.IntegerField()
    n2_5 = models.IntegerField()
    mg44_5 = models.IntegerField()
    n2_6 = models.IntegerField()
    m33_6 = models.IntegerField()
    sum_m = models.IntegerField()
    sum_n2 = models.IntegerField()
    fold_change = models.FloatField(blank=True)
    log2 = models.FloatField(blank=True)
    expressed = models.BooleanField(blank=True)
    p_value = models.FloatField(blank=True)

    def __unicode__(self):
        return self.ensembl_id

    class Meta:
       verbose_name = "PI3K/age-1 m vs. N2"
       verbose_name_plural = verbose_name
    

class PI3K(models.Model):
    entrez_gene_id = models.IntegerField(blank=True, null=True)
    ensembl_id = models.CharField(max_length=23, blank=True)
    special = models.FloatField(blank=True, null=True)

    symbol = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=50, blank=True)
    
    N2_sum = models.FloatField(blank=True, null=True)
    N2_average = models.FloatField(blank=True, null=True)
    N2_variance = models.FloatField(blank=True, null=True)

    hx_sum = models.FloatField(blank=True, null=True)
    hx_average = models.FloatField(blank=True, null=True)
    hx_variance = models.FloatField(blank=True, null=True)
    
    m_sum = models.FloatField(blank=True, null=True)
    m_average = models.FloatField(blank=True, null=True)
    m_variance = models.FloatField(blank=True, null=True)
    
    m_N2_fold_change = models.FloatField(blank=True, null=True)
    m_hx_fold_change = models.FloatField(blank=True, null=True)
    hx_N2_fold_change = models.FloatField(blank=True, null=True)

    m_N2_p_value = models.FloatField(blank=True, null=True)
    m_hx_p_value = models.FloatField(blank=True, null=True)
    hx_N2_p_value = models.FloatField(blank=True, null=True)

##    m_N2_paired_p_value = models.FloatField(blank=True, null=True)
##    m_hx_paired_p_value = models.FloatField(blank=True, null=True)
##    hx_N2_paired_p_value = models.FloatField(blank=True, null=True)
    
    log2 = models.FloatField(blank=True, null=True)
    expressed = models.BooleanField(blank=True)

    def __unicode__(self):
        return self.ensembl_id

    class Meta:
        verbose_name = "PI3K age-1 m & hx vs. N2"
        verbose_name_plural = verbose_name


class germline_expressed_genes(models.Model):
    ensembl_id = models.CharField(max_length=11)
    symbol = models.CharField(max_length=9)
    chr = models.CharField(max_length=5)
    germline_tags = models.IntegerField()

    def __unicode__(self):
        return self.symbol

    class Meta:
        verbose_name = "germline expressed gene"


class Germline_specific_genes(models.Model):
    ensembl_id = models.CharField(max_length=10)
    symbol = models.CharField(max_length=8)
    germline_tags = models.IntegerField()
    in_situ = models.CharField(max_length=3)
    sage = models.CharField(max_length=1)
    microarray = models.CharField(max_length=1)
    rnai = models.CharField(max_length=40)
    descriptions = models.CharField(max_length=65)

    def __unicode__(self):
        return self.ensembl_id

    class Meta:
        verbose_name = "germline-specific gene"
   

class IME1_overexpression(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True) #empty
    nucleotide_title = models.CharField(max_length=1, blank=True) #empty
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True) #empty
    go_component_id = models.CharField(max_length=144, blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=10)
    platform_cloneid = models.CharField(max_length=1, blank=True) #empty
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True) #empty
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True) #empty
    unigene_symbol = models.CharField(max_length=1, blank=True) #empty
    platform_spotid = models.CharField(max_length=1, blank=True) #empty
    go_function_id = models.CharField(max_length=217, blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True) #empty
    fold_change = models.FloatField()
    change_1 = models.FloatField()
    change_2 = models.FloatField()
    p_value = models.FloatField()

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "IME1 overexpression"
        verbose_name_plural = verbose_name


class NDT80_knockout(models.Model):
    orf = models.CharField(max_length=9)
    fold_change = models.FloatField()
    p_value = models.FloatField()

    def __unicode__(self):
        return self.orf

    class Meta:
        verbose_name = "NDT80 knockout"
        verbose_name_plural = verbose_name


class NDT80_overexpression(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True) #empty
    nucleotide_title = models.CharField(max_length=1, blank=True)   #empty
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True) #empty
    go_component_id = models.CharField(max_length=144, blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=10)
    platform_cloneid = models.CharField(max_length=1, blank=True)   #empty
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True)   #empty
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True)   #empty
    unigene_symbol = models.CharField(max_length=1, blank=True)    #empty
    platform_spotid = models.CharField(max_length=1, blank=True)   #empty
    go_function_id = models.CharField(max_length=217, blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True)   #empty
    fold_change = models.FloatField()
    change_1 = models.FloatField()
    change_2 = models.FloatField()
    p_value = models.FloatField()

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "NDT80 overexpression"
        verbose_name_plural = verbose_name


class Yeast_TF_binding(models.Model):
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
        verbose_name = "yeast TF-binding"


class Sporulation_2h_vs_0(models.Model):
    probe_id = models.IntegerField()
    unigene_title = models.CharField(max_length=1, blank=True) #Empty
    nucleotide_title = models.CharField(max_length=1, blank=True) #Empty
    go_component = models.TextField(blank=True)
    unigene_id = models.CharField(max_length=1, blank=True) #Empty
    go_component_id = models.CharField(max_length=192, blank=True)
    chromosome_annotation = models.CharField(max_length=58, blank=True)
    go_function = models.TextField(blank=True)
    platform_orf = models.CharField(max_length=10, blank=True)
    platform_cloneid = models.CharField(max_length=1, blank=True) #Empty
    go_process_id = models.TextField(blank=True)
    genbank_accession = models.CharField(max_length=1, blank=True) #Empty
    gene_symbol = models.CharField(max_length=10, blank=True)
    go_process = models.TextField(blank=True)
    entrez_gene_id = models.IntegerField(blank=True)
    gi = models.CharField(max_length=1, blank=True) #Empty
    unigene_symbol = models.CharField(max_length=1, blank=True) #Empty
    platform_spotid = models.CharField(max_length=11, blank=True)
    go_function_id = models.TextField(blank=True)
    gene_name = models.CharField(max_length=240, blank=True)
    chromosome_location = models.CharField(max_length=1, blank=True) #Empty
    fold_change = models.FloatField()

    def __unicode__(self):
        return self.gene_symbol
   
    class Meta:
        verbose_name = "Sporulation 2h vs. 0h"
        verbose_name_plural = verbose_name
    

class NDT80ER(models.Model):
    orf = models.CharField(max_length=9)
    ndt80_9h_1_pvalue = models.FloatField(blank=True)
    ndt80_9h_1_ratio = models.FloatField(blank=True)
    ndt80_9h_2_pvalue = models.FloatField(blank=True)
    ndt80_9h_2_ratio = models.FloatField(blank=True)
    avearge_ratio_ndt80_9h = models.FloatField(blank=True)
    ndt80_zscore = models.FloatField(blank=True)
    ndt80_binding_zscore_077 = models.IntegerField(blank=True)
    ndt80_site = models.FloatField(blank=True)
    sum1_15h_1_pvalue = models.FloatField(blank=True)
    sum1_15h_1_ratio = models.FloatField(blank=True)
    sum1_15h_2_pvalue = models.FloatField(blank=True)
    sum1_15h_2_ratio = models.FloatField(blank=True)
    avearge_sum1_15h = models.FloatField(blank=True)
    sum1zscore = models.FloatField(blank=True)
    sum1_binding = models.IntegerField()
    sum1_site = models.FloatField(blank=True)
    ndt80_only = models.IntegerField(blank=True)
    common = models.IntegerField(blank=True)
    sum1_only = models.IntegerField(blank=True)
    harbison_2004_sum1_chip_on_chip_in_ypd_pvalue = models.FloatField(blank=True)
    wang_2005_ndt80_tar = models.IntegerField()
    wang_2005_sum1_tar = models.IntegerField()
    pierce_2003_sum1_derepressed = models.IntegerField()
    chu_1998_over_2_in_ndt80oe = models.IntegerField()
    primig_2000_cluster1 = models.IntegerField()
    primig_2000_cluster2 = models.IntegerField()
    primig_2000_cluster3 = models.IntegerField()
    primig_2000_cluster4 = models.IntegerField()
    primig_2000_cluster5 = models.IntegerField()
    primig_2000_cluster6 = models.IntegerField()
    primig_2000_cluster7 = models.IntegerField()
    primig_2000_cluster8 = models.IntegerField()
    primig_2000_cluster9 = models.IntegerField()
    primig_2000_cluster10 = models.IntegerField()
    mrna_0h = models.FloatField(blank=True)
    mrna_1h = models.FloatField(blank=True)
    mrna_2h = models.FloatField(blank=True)
    mrna_3h = models.FloatField(blank=True)
    mrna_4h = models.FloatField(blank=True)
    mrna_5h = models.FloatField(blank=True)
    mrna_6h = models.FloatField(blank=True)
    mrna_7h = models.FloatField(blank=True)
    mrna_8h = models.FloatField(blank=True)
    mrna_9h = models.FloatField(blank=True)
    mrna_10h = models.FloatField(blank=True)
    mrna_11h = models.FloatField(blank=True)
    mrna_12h = models.FloatField(blank=True)
    mrna_13h = models.FloatField(blank=True)
    mrna_14h = models.FloatField(blank=True)
    mrna_15h = models.FloatField(blank=True)
    mrna_16h = models.FloatField(blank=True)
    mrna_17h = models.FloatField(blank=True)
    mrna_18h = models.FloatField(blank=True)
    cluster = models.IntegerField(blank=True)
    before_deconvolution_0h = models.FloatField(blank=True)
    before_deconvolution_14 = models.FloatField(blank=True)
    before_deconvolution_18 = models.FloatField(blank=True)
    sum1_deletion_10h = models.FloatField(blank=True)
    sum1_deletion_17h = models.FloatField(blank=True)
    sum1_deletion_21h = models.FloatField(blank=True)
    ndt80er_0h = models.FloatField(blank=True)
    ndt80er_8h = models.FloatField(blank=True)
    ndt80er_14h = models.FloatField(blank=True)

    def __unicode__(self):
        return self.orf

    class Meta:
        verbose_name = "NDT80 ergosterone induced"
        verbose_name_plural = verbose_name


class CeMM(models.Model):
    ensembl = models.CharField(max_length=20)
    array_1 = models.FloatField(blank=True)
    array_2 = models.FloatField(blank=True)
    array_3 = models.FloatField(blank=True)
    pmid = 17023606 
    taxid = 6230
    info = "Negative value = down in CeMM"

    def __unicode__(self):
        return self.ensembl  

    class Meta:
       verbose_name = "CeMM"
       verbose_name_plural = "CeMM"


class TemporalLinkageDR(models.Model):
    genbank = models.CharField(max_length=8)
    symbol = models.CharField(max_length=12)
    cr2 = models.FloatField(blank=True)
    cr4 = models.FloatField(blank=True)
    cr8 = models.FloatField(blank=True)
    lt_cr = models.FloatField()
    con8 = models.FloatField(blank=True)
    gene_class = models.CharField(max_length=11)
    category = models.CharField(max_length=38)
    pmid = 15044709
    taxid = 10090
    tissue = 'liver'

    def __unicode__(self):
        return self.symbol  

    class Meta:
         verbose_name = "Temporal linkage DR"
         verbose_name_plural = verbose_name


class AlteredGeneExpressionInCeMM(models.Model):
    fold_change = models.CharField(max_length=9)
    ensembl = models.CharField(max_length=9)
    mountain = models.CharField(max_length=4)
    description = models.CharField(max_length=88)
    regulation = models.CharField(max_length=4)
    pmid = 17023606 
    taxid = 6230

    def __unicode__(self):
        return self.ensembl  

    class Meta:
       verbose_name = "Altered gene expression in CeMM"
       verbose_name_plural = verbose_name     
