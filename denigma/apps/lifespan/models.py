from django.db import models
from django.utils.translation import ugettext_lazy as _

from datasets.models import Reference


class Study(models.Model):
    """A lifespan study."""
    pmid = models.IntegerField(blank=True, null=True, unique=True)
    title = models.CharField(max_length=250, blank=True, null=True, unique=True)
    link = models.URLField(blank=True, null=True)
    reference = models.ForeignKey(Reference, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    integrated = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #experiments = models.OneToMany(Experiment) # ForeignKey?
    
    def __unicode__(self):
        if self.reference:
            return self.reference.__unicode__()
        else:
            return "{0} {1}".format(self.pmid, self.title)

    class Meta():
        verbose_name_plural = "studies"

    def save(self, *args, **kwargs):
        """Check whether study is already in references and fetches annotation."""
        kwargs['title'] = self.title
        kwargs['pmid'] = self.pmid
        if self.link:
           kwargs['link'] = self.link
        reference, created = Reference.objects.get_or_create(*args, **kwargs)
        self.pmid = reference.pmid
        self.title = reference.title
        self.reference = reference
        super(Study, self).save()


class Experiment(models.Model):
    """A lifespan experiment."""
    name = models.CharField(max_length=250, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    study = models.ForeignKey(Study)
    species = models.ForeignKey('annotations.Species')
    def __unicode__(self):
        return self.name


class Strain(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
         return self.name


class Measurement(models.Model):
    """A lifespan measurment from a table or graph."""
    experiment = models.ForeignKey(Experiment)
    comparisions = models.ManyToManyField("self", through="Comparision", symmetrical=False)
    control = models.BooleanField()

    strain = models.ForeignKey(Strain, blank=True, null=True) # Genetic background.
    genotype = models.CharField(max_length=50, blank=True, null=True) # Wild-type or mutant.
    diet = models.CharField(max_length=150, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    start = models.FloatField(blank=True, null=True) # Start age of treatment.

    # Lifespan measurement type:
    mean = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)   # Maximum lifespan
    num = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
         return u"{0} {1}".format(self.genotype, self.diet)


class Epistasis(models.Model):
    """A possible enhancement of the restricted choices field."""
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
     
    class Meta:
        verbose_name_plural = "epistases"


class Comparision(models.Model):
    """A comparision between two lifespan measurements."""
    #EPISTATIC = (
    #    (1, _('Neutral')),
    #    (2, _('Addative')),
    #    (3, _('Multiplicative'))
    #           )
    experimental = models.ForeignKey(Measurement, related_name="experimental_group")
    control = models.ForeignKey(Measurement, related_name="control_group")
    #epistasis = models.PositiveSmallIntegerField(max_length=1, blank=True, null=True, choices=EPISTATIC)
    epistasis = models.ForeignKey(Epistasis, blank=True, null=True)
    intervention = models.ForeignKey('Intervention', blank=True, null=True) # ManyToMany?
    mean = models.FloatField(blank=True, null=True) # Mean lifespan extension.
    median = models.FloatField(blank=True, null=True) # Median lifespan extension.
    max = models.FloatField(blank=True, null=True) # Maximum lifespan extension.#

    def __unicode__(self):
        return u"{0} vs. {1}".format(self.experimental.genotype, self.control.genotype)


## Migrated to lifespan:


class Type(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name


class Regimen(models.Model):
    name = models.CharField(max_length=40)
    shortcut = models.CharField(max_length=20)
    description = models.TextField()
    def __unicode__(self):
        return self.shortcut


class Assay(models.Model):
    name = models.CharField(max_length=40)
    shortcut = models.CharField(max_length=20)

    def __unicode__(self):
        return self.shortcut


class Manipulation(models.Model):
    shortcut = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.ManyToManyField('self', symmetrical=False, related_name='type_of', blank=True)
    #type = models.ManyToManyField('self', through='ManipulationType', symmetrical=False, related_name='type_of', blank=True)

##    def add_manipulation_type(self, manipulation):
##        relationship
    
    def __unicode__(self):
        return self.name

##class ManipulationType(models.Model):
##    from_manipulation = models.ForeignKey(Manipulation, related_name='from_manipulation')
##    to_manipulation = models.ForeignKey(Manipulation, related_name='to_manipulation')
##
##    class Meta():
##        db_table = u'manipulation_type'
##        

class Intervention(models.Model):
    name = models.CharField(max_length=250)
    taxid = models.IntegerField(blank=True, null=True)
    background = models.CharField(max_length=250, blank=True)
    sex = models.CharField(max_length=25, blank=True)
    lifespans = models.CharField(max_length=25, blank=True)
    effect = models.TextField(blank=True)
    mean = models.CharField(max_length=15, null=True, blank=True)
    median = models.CharField(max_length=15, null=True, blank=True)
    _25 = models.CharField(max_length=15, null=True, blank=True)
    _75 = models.CharField(max_length=15, null=True, blank=True)
    maximum = models.CharField(max_length=15, null=True, blank=True)
    pmid = models.CharField(max_length=250, blank=True)
    references = models.ManyToManyField('datasets.Reference', blank=True)
    manipulation = models.ManyToManyField(Manipulation, blank=True)
    
##    species = models.ManyToManyField(Species)
    def __unicode__(self):
        return self.name


class Factor(models.Model):  # Rename to Entity AgeFactor
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    #geneid = models.ForeignKey(Gene, blank=True)   # Or Genes
    mapping = models.IntegerField(null=True, blank=True)
    ensembl_gene_id = models.CharField(max_length=18, blank=True)
    symbol = models.CharField(max_length=13, blank=True)   # Rename to symbol.
    name = models.CharField(max_length=244, blank=True)    # Rename to name.
    alias = models.CharField(max_length=270, blank=True)
    function = models.TextField(blank=True)    # Manually curated functional description field.
    description = models.TextField(blank=True) # Automatically populated field for functional descriptions.
    functional_description = models.TextField(blank=True)    
    observation = models.TextField(blank=True)
    classification = models.CharField(max_length=20, blank=True)
    classifications = models.ManyToManyField('annotations.Classification')
    regimen = models.ManyToManyField(Regimen, blank=True)
    assay = models.ManyToManyField(Assay)
    diet_regimen = models.CharField(max_length=250, blank=True)
    life_span = models.CharField(max_length=250, blank=True)   
    taxid = models.IntegerField(null=True, blank=True)
    #species = models.ManyToManyField(Taxonomy)
    pubmed_id = models.CharField(max_length=250, blank=True)
    reference = models.CharField(max_length=250, blank=True)
    references = models.ManyToManyField('datasets.Reference', blank=True)
    mean = models.CharField(max_length=15, null=True, blank=True)
    median = models.CharField(max_length=15, null=True, blank=True)
    maximum = models.CharField(max_length=15, null=True, blank=True)
    _75 = models.CharField('75%ile', max_length=15, null=True, blank=True)
    _25 = models.CharField('25%lie', max_length=15, null=True, blank=True)
    manipulation = models.CharField(max_length=250, null=True, blank=True)
    intervention = models.ManyToManyField(Intervention, blank=True)
    gene_intervention = models.CharField(max_length=250, null=True, blank=True)
    synergistic_epistasis = models.CharField(max_length=33, blank=True)
    antagonistic_epistasis = models.CharField(max_length=216, blank=True)
    human_homologue = models.CharField(max_length=18, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=25, null=True, blank=True) # Gene, or drug
    types = models.ManyToManyField(Type, blank=True)
    
    
    def __unicode__(self):
        return self.symbol

    def data(self):
        return self.entrez_gene_id, self.symbol, self.name, self.alias

    data = property(data)
