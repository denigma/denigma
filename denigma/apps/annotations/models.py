from django.db import models


class Taxonomy(models.Model):
    superkingdom = models.CharField(max_length=54, blank=True)
    tribe = models.CharField(max_length=87, blank=True)
    litter_rate = models.IntegerField(null=True, blank=True)
    subgenus = models.CharField(max_length=93, blank=True)
    acronyms = models.CharField(max_length=147, blank=True)
    family = models.CharField(max_length=129, blank=True)
    adult_weight = models.FloatField(null=True, blank=True)
    scientific_name = models.CharField(max_length=324, blank=True)
    litters_size = models.FloatField(null=True, blank=True)
    synonyms = models.TextField(blank=True)
    phylum = models.CharField(max_length=102, blank=True)
    superclass = models.CharField(max_length=45, blank=True)
    body_mass = models.FloatField(null=True, blank=True)
    classis = models.CharField(max_length=84, blank=True)
    specimen_origin = models.CharField(max_length=27, blank=True)
    subspecies = models.CharField(max_length=111, blank=True)
    genbank_anamorph = models.CharField(max_length=117, blank=True)
    genbank_synonym = models.CharField(max_length=168, blank=True)
    ordo = models.CharField(max_length=129, blank=True)
    forma = models.CharField(max_length=135, blank=True)
    common_names = models.CharField(max_length=534, blank=True)
    misnomers = models.CharField(max_length=687, blank=True)
    inter_litters = models.IntegerField(null=True, blank=True)
    infraorder = models.CharField(max_length=54, blank=True)
    subclass = models.CharField(max_length=93, blank=True)
    equivalent_names = models.TextField(blank=True)
    source = models.CharField(max_length=129, blank=True)
    imr = models.FloatField(null=True, blank=True)
    superphylum = models.CharField(max_length=24, blank=True)
    metabolic_rate = models.FloatField(null=True, blank=True)
    species_subgroup = models.CharField(max_length=84, blank=True)
    anamorphs = models.CharField(max_length=213, blank=True)
    growth_rate = models.FloatField(null=True, blank=True)
    kingdom = models.CharField(max_length=36, blank=True)
    mrdt = models.FloatField(null=True, blank=True)
    weaning_weight = models.FloatField(null=True, blank=True)
    genbank_acronym = models.CharField(max_length=66, blank=True)
    subtribe = models.CharField(max_length=87, blank=True)
    weaning_days = models.IntegerField(null=True, blank=True)
    genbank_common_name = models.CharField(max_length=171, blank=True)
    subphylum = models.CharField(max_length=93, blank=True)
    subkingdom = models.CharField(max_length=15, blank=True)
    unpublished_names = models.CharField(max_length=381, blank=True)
    gestation = models.IntegerField(null=True, blank=True)
    includes = models.TextField(blank=True)
    infraclass = models.CharField(max_length=42, blank=True)
    male_maturity = models.IntegerField(null=True, blank=True)
    varietas = models.CharField(max_length=141, blank=True)
    no_rank = models.CharField(max_length=204, blank=True)
    teleomorph = models.CharField(max_length=117, blank=True)
    reference = models.CharField(max_length=531, blank=True)
    authorities = models.TextField(blank=True)
    subfamily = models.CharField(max_length=57, blank=True)
    female_maturity = models.IntegerField(null=True, blank=True)
    in_parts = models.CharField(max_length=366, blank=True)
    superorder = models.CharField(max_length=54, blank=True)
    superfamily = models.CharField(max_length=84, blank=True)
    birth_weight = models.FloatField(null=True, blank=True)
    taxid = models.IntegerField(null=True, blank=True)
    blast_name = models.CharField(max_length=75, blank=True)
    maximum_longevity = models.FloatField(null=True, blank=True)
    sample_size = models.CharField(max_length=18, blank=True)
    parvorder = models.CharField(max_length=42, blank=True)
    species_group = models.CharField(max_length=84, blank=True)
    data_quality = models.CharField(max_length=36, blank=True)
    suborder = models.CharField(max_length=93, blank=True)
    species = models.CharField(max_length=228, blank=True)
    genus = models.CharField(max_length=147, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    misspellings = models.TextField(blank=True)

    class Meta:
        db_table = u'taxonomy'

    def __unicode__(self):
        return u"{0} {1}".format(self.taxid, self.scientific_name)
        
##class Classsification(models.Model):
##    name = models.CharField(max_length=20)
##
##class Gene(models.Model):
##    entrez_gene_id = models.IntegerField(primary_key=True)
##    models.ManyToManyField(Classification)

class Animal(models.Model):
    alternative_names = models.CharField(max_length=21, blank=True) # Field name made lowercase.
    taxid = models.IntegerField(null=True, blank=True) # Field name made lowercase.
    def __unicode__(self):
        return self.alternative_names

class Species(models.Model):
    taxid = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=7, blank=True)
    common_name = models.CharField(max_length=14, blank=True)
    alternative_names = models.ManyToManyField(Animal)
    latin_name = models.CharField(max_length=25, blank=True)
    latin_shortcut = models.CharField(max_length=15, blank=True)
    number_genes = models.IntegerField(null=True, blank=True)
    gendr_genes = models.IntegerField(null=True, blank=True)
    gendr_orthologs = models.IntegerField(null=True, blank=True)
    gendr_paralogs = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.common_name 

##class Taxonomy(models.Model):
##    taxid = models.IntegerField(primary_key=True)
##    short_name = models.CharField(max_length=7, blank=True)
##    common_name = models.CharField(max_length=14, blank=True)
##    alternative_names = models.ManyToManyField(Animal)
##    latin_name = models.CharField(max_length=25, blank=True)
##    latin_shortcut = models.CharField(max_length=15, blank=True)
##    number_genes = models.IntegerField(null=True, blank=True)
##    gendr_genes = models.IntegerField(null=True, blank=True)
##    gendr_orthologs = models.IntegerField(null=True, blank=True)
##    gendr_paralogs = models.IntegerField(null=True, blank=True)    
##        class Meta()
##        db_table = u'Taxonomy'

class DiscontinuedId(models.Model):
    discontinued_id = models.IntegerField(primary_key=True)
    entrez_gene_id = models.IntegerField()
    def __unicode__(self):
        return u'%s, %s' % (self.discontinued_id, self.entrez_gene_id)

class Candidate(models.Model):
    entrez_gene_id = models.IntegerField()
    gene_symbol = models.CharField(max_length=40, blank=True)
    gene_name = models.TextField(blank=True)
    t = models.IntegerField()
    s = models.IntegerField()
    specificity =  models.FloatField(null=True, blank=True)
    p_value = models.FloatField(db_column='p-Value', null=True, blank=True)
    taxid = models.IntegerField()
    query = models.CharField(max_length = 50)
    classification = models.CharField(max_length = 30)    
    seed = models.BooleanField()
    yeast_homolog_id = models.CharField(max_length = 500, default='', blank=True)
    worm_homolog_id = models.CharField(max_length = 500, default='', blank=True)
    fly_homolog_id = models.CharField(max_length = 500, default='', blank=True)
    mouse_homolog_id = models.CharField(max_length = 500, default='', blank=True)
    rat_homolog_id = models.CharField(max_length = 500, default='',  blank=True)
    human_homolog_id = models.CharField(max_length = 500, default='', blank=True)
    yeast_homolog_symbol = models.CharField(max_length = 500, default='', blank=True)
    worm_homolog_symbol = models.CharField(max_length = 500, default='', blank=True)
    fly_homolog_symbol = models.CharField(max_length = 500, default='' , blank=True)
    mouse_homolog_symbol = models.CharField(max_length = 500, default='', blank=True)
    rat_homolog_symbol = models.CharField(max_length = 500, default='', blank=True)
    human_homolog_symbol = models.CharField(max_length = 500, default='', blank=True)
    dr = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'Candidate'

class Entrez(models.Model):
    entrez_gene_id = models.IntegerField(primary_key=True)
    gene_symbol = models.CharField(max_length=32, blank=True)
    gene_name = models.TextField(blank=True)
    locus_tag = models.CharField(max_length=25, blank=True)
    symbol_from_nomeclature_authority = models.CharField(max_length=29, blank=True)
    full_name_from_nomenclature_autority = models.CharField(max_length=251, blank=True)
    ensembl_gene_id = models.CharField(max_length=18, blank=True)
    mirbase = models.CharField(max_length=9, blank=True)
    mgi = models.CharField(max_length=11, blank=True)
    hgnc = models.IntegerField()
    mim = models.IntegerField()
    hprd = models.IntegerField()
    rgd = models.IntegerField()
    ratmap = models.CharField(max_length=1, blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    imgt_gene_db = models.CharField(max_length=16, blank=True)
    taxid = models.IntegerField()


class GO(models.Model):
    taxid = models.IntegerField()
    entrez_gene_id = models.IntegerField()
    go_id = models.CharField(max_length=10)
    evidence = models.CharField(max_length=3)
    qualifier = models.CharField(max_length=20, blank=True)
    go_term = models.CharField(max_length=193)
    pmid = models.CharField(max_length=17, blank=True)
    category = models.CharField(max_length=9)
    def __unicode__(self):
        return u'%s, %s %s %s' % (self.go_id, self.go_term, self.entrez_gene_id, entrez_gene_id)


class SGD_features(models.Model):
    sgd_id = models.CharField(max_length=10)
    feature_type = models.CharField(max_length=35)
    feature_qualifier = models.CharField(max_length=22, blank=True)
    ensembl_gene_id = models.CharField(max_length=11, blank=True)
    gene_symbol = models.CharField(max_length=10, blank=True)
    alias = models.CharField(max_length=63, blank=True)
    parent_feature_name = models.CharField(max_length=13)
    secondary_sgd_id = models.CharField(max_length=54, blank=True)
    chromosome = models.IntegerField(blank=True)
    start_coordinate = models.IntegerField(blank=True)
    stop_coordinate = models.IntegerField(blank=True)
    strand = models.CharField(max_length=1,blank=True)
    genetic_position = models.FloatField(blank=True)
    coordinate_version = models.DateField(blank=True)#max_length=10
    sequence_version = models.CharField(max_length=43)
    description = models.TextField(blank=True)

class SGD_gene_association(models.Model):
    sgd_id = models.CharField(max_length=10)
    gene_symbol = models.CharField(max_length=10)
    with_or_from = models.CharField(max_length=16, blank=True)
    go_id = models.CharField(max_length=10)
    reference = models.CharField(max_length=32)
    evidence = models.CharField(max_length=3)
    other_ids = models.TextField(blank=True)
    category = models.CharField(max_length=1)
    gene_name = models.CharField(max_length=72)
    orf = models.CharField(max_length=54)
    date = models.IntegerField()
    source = models.CharField(max_length=9)

class Classification(models.Model):
    title = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    shortcut = models.CharField(max_length=5)
    def __unicode__(self):
        return self.title

class Gene(models.Model):
    entrez_gene_id = models.IntegerField(primary_key=True)
    taxid = models.IntegerField()
    classification = models.ManyToManyField(Classification)
    gene_symbol = models.CharField(max_length=30, blank=True)
    classes = models.CharField(max_length=30, blank=True)

class HomoloGene(models.Model):
    hid = models.IntegerField()
    taxid = models.IntegerField()
    entrez_gene_id = models.IntegerField()
    gene_symbol = models.CharField(max_length=42)
    protein_gi = models.IntegerField()
    protein_accession = models.CharField(max_length=14)

class Entry(models.Model):
    name = models.CharField(max_length=10)
    
class Blog(models.Model):
    entry = models.ManyToManyField(Entry)
    title = models.CharField(max_length=10)
    
##class EnsemblHomolog(models.Model):
##    ensembl_gene_id_a = models.CharField(max_length=18, db_index=True)
##    ensembl_gene_id_b = models.CharField(max_length=18, db_index=True)
##    homology_type = models.CharField(max_length=25, db_index=True)
##    ds = models.FloatField(blank=True)
##    dn = models.FloatField(blank=True)
##    percentage_identity_a = models.IntegerField()
##    percentage_identity_b = models.IntegerField()
##    taxid_a = models.IntegerField()
##    taxid_b = models.IntegerField()
##    potential_homolog = models.BooleanField()

class InParanoid(models.Model):
    group_number = models.IntegerField()
    ensembl_gene_id_a = models.CharField(max_length=20)
    ensembl_gene_id_b = models.CharField(max_length=20)
    taxid_a = models.IntegerField()
    taxid_b = models.IntegerField()

class gene2ensembl(models.Model):
    taxid = models.IntegerField(db_index=True)
    entrez_gene_id = models.IntegerField(db_index=True)
    ensembl_gene_id = models.CharField(max_length=18, db_index=True)
    rna_nucleotide_accession = models.CharField(max_length=14)
    ensembl_rna_id = models.CharField(max_length=18)
    protein_accession = models.CharField(max_length=14)
    ensembl_protein_id = models.CharField(max_length=18)

class EnsemblEntrezGeneId(models.Model):
    ensembl_gene_id = models.CharField(max_length=18)
    entrez_gene_id = models.IntegerField()
    taxid = models.IntegerField()

class Gen(models.Model):
    entrez_gene_id = models.IntegerField(primary_key=True)
    gene_symbol = models.CharField(max_length=40, blank=True)
    gene_name = models.CharField(max_length=173, blank=True)
    taxid = models.IntegerField()
    classification = models.CharField(max_length=33)
    ageing_associated = models.BooleanField()
    positive_gerontogene = models.BooleanField()
    negative_gerontogene = models.BooleanField()
    positive_ageing_suppressor = models.BooleanField()
    negative_ageing_suppressor = models.BooleanField()
    longevity_associated = models.BooleanField()
    ageing_differential = models.BooleanField()
    ageing_induced = models.BooleanField()
    ageing_suppressed = models.BooleanField()
    dr_essential = models.BooleanField()
    dr_differential = models.BooleanField()
    dr_induced = models.BooleanField()
    dr_suppressed = models.BooleanField()
    core_clock = models.BooleanField()
    clock_modulator = models.BooleanField()
    circadian_differential = models.BooleanField()
    clock_systemic = models.BooleanField()
    juvenile_differential = models.BooleanField()
    juvenile_induced = models.BooleanField()
    juvenile_suppressed = models.BooleanField()
    embryonic_lethal = models.BooleanField()
    senescence_differential = models.BooleanField()
    senescence_induced = models.BooleanField()
    senescence_suppressed = models.BooleanField()
    gerontogene = models.BooleanField()
    ageing_suppressor = models.BooleanField()
    imprinted = models.BooleanField()
    maternal_imprinted = models.BooleanField()
    paternal_imprinted = models.BooleanField()
    transcription_factor = models.BooleanField()
    pacemaker = models.BooleanField()
    high_amplitude = models.BooleanField()
    short_period = models.BooleanField()
    long_period = models.BooleanField()
    juvenile_associated = models.BooleanField()
    ageing_methylated = models.BooleanField()
    dr_essential_ortholog = models.BooleanField()
    clock_modulator_ortholog = models.BooleanField()


class Ortholog(models.Model):
    ortholog = models.IntegerField()
    ortholog_symbol = models.CharField(max_length=20, blank=True)
    ortholog_taxid = models.IntegerField()
    gene = models.IntegerField()
    gene_symbol = models.CharField(max_length=20, blank=True)
    gene_taxid = models.IntegerField()

class Entrez_Gene(models.Model):
    entrez_gene_id = models.IntegerField(primary_key = True)
    gene_symbol = models.CharField(max_length=32)
    gene_name = models.CharField(max_length=1, blank=True) # Is empty!!!!
    locus_tag = models.CharField(max_length=25, blank=True)
    symbol_from_nomenclature_authority = models.CharField(max_length=29, blank=True)
    full_name_from_nomenclature_autority = models.CharField(max_length=251, blank=True)
    ensembl_gene_id = models.CharField(max_length=18, blank=True)
    mirbase = models.CharField(max_length=9, blank=True)
    mgi = models.CharField(max_length=11, blank=True)
    hgnc = models.IntegerField(blank=True)
    mim = models.IntegerField(blank=True)
    hprd = models.IntegerField(blank=True)
    rgd = models.IntegerField(blank=True)
    ratmap = models.CharField(max_length=1, blank=True) # Is empty!!!!
    wormbase_id = models.CharField(max_length=14, blank=True)
    imgt_gene_db = models.CharField(max_length=16, blank=True)
    taxid = models.IntegerField()

##class member(models.Model):
##    member_id = models.IntegerField() #Too long, should be integer
##    stable_id = models.CharField(max_length=19) #Should be varchar(40)
##    version = models.IntegerField()
##    source_name = models.CharField(max_length=17) #Should be varchar(40)
##    taxon_id = models.IntegerField()
##    genome_db_id = models.IntegerField(blank=True) #Should be integer
##    sequence_id = models.IntegerField(blank=True)
##    gene_member_id = models.IntegerField()
##    description = models.TextField(blank=True)
##    chr_name = models.CharField(max_length=27)  #Should be varchar(40)
##    chr_start = models.IntegerField()
##    chr_end = models.IntegerField()
##    chr_strand = models.IntegerField()
##    display_label = models.CharField(max_length=12)
##    entrez_gene_id = models.IntegerField(null=True, blank=True)
##    mapping = models.IntegerField(blank=True, null=True)
##    def __unicode__(self):
##        return self.stable_id

##class homology(models.Model):
##    homology_id = models.IntegerField(primary_key=True)
##    stable_id = models.CharField(max_length=40)	 	
##    method_link_species_set_id = models.IntegerField() 	
##    description = models.CharField(max_length=40) 	 	
##    subtype = models.CharField(max_length=40) 	 	 	 	 	 	
##    dn = models.FloatField()
##    ds = models.FloatField()
##    n = models.FloatField()
##    s = models.FloatField()
##    lnl = models.FloatField()
##    threshold_on_ds = models.FloatField()	 	
##    ancestor_node_id = models.IntegerField()	 	 	
##    tree_node_id = models.IntegerField()
##    def __unicode__(self):
##        return self.stable_id

##class homologs(models.Model):
##    entrez_gene_a = models.IntegerField()
##    entrez_gene_b = models.IntegerField()
##    ensembl_gene_a varchar(20),
##    ensembl_gene_b varchar(20),
##    ensembl_protein_a varchar(20),
##    ensembl_protein_b varchar(20),
##    category varchar(255),
##    group_num varchar(255),
##    dn int,
##    ds int,
##    n int,
##    s int,
##    taxid_a int NOT NULL,
##    taxid_b int NOT NULL,
##    db varchar(38) NOT NULL,
##    score int NOT NULL)'''

    
##class Entity(models.Model):
##    """An entity which can be everything which has attributes."""
##    #type = models.Choice(# or M2M
##    name = models.CharField(max_length=250)
##    db = model.ForeignKey(DB)
##    attributes = model.ManyToManyField(Attribute)
##    entity = models.ManyToManyField('Entity')
##    modification = models.ManyToManyField('Modification')

##class Relation(models.Model):
##    a = models.ForeignKey(Entity, related_name='source') # parent
##    b = models.ForeignKey(Entity, related_name='target') # child
##    name = model.CharField(max_length=250)
##    description = models.TextField(blank=True)
##    directed = models.BooleanField()
##    modification = models.ManyToManyField('Modification')

##class Modification(models.Model):
##    pass

##class DB(models.Model):
##    """A source DB."""
##    name = models.CharField()
##    description = models.TextField()
##
##class Attribute(models.Model):
##    name = models.CharField()
##    value = models.CharField()
