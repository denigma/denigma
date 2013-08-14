# -*- coding: utf-8 -*-
import re

from django.db import models, IntegrityError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.signals import m2m_changed
from django.core.urlresolvers import reverse

from datasets.models import Reference

try:
    from annotations.mapping import m
    from annotations.models import Entrez, Species
    from annotations.SGD.yeastmine import retrieve
    MAPPING = True
except:
    MAPPING = False

import handlers


WT = ['wt', 'WT' 'wild type']



class VariantManager(models.Manager):
    def get_queryset(self):
        return self.model.objects.exclude(choice__name__contains='Review')


class StateManager(models.Manager):
    def get_queryset(self):
        print("get queryset")
        return self.model.objects.exclude(variant__choice__name__contains='Review')


# Helper functions:
def examine(value):
    """Examines a string value whether it is None, float, or int."""
    if value and value in ['-', 'N.A.']:
        value = None
    elif "." in value:
        try:
            return float(value)
        except ValueError:
            try:
                return int(value)
            except ValueError:
                return value
    else:
        try:
            return int(value)
        except ValueError:
            return value

def multi_replace(string, items, by):
    """Performs a multiple replacements of a sequence of string by another common string."""
    for item in items:
        string = string.replace(item, by)
    return string

def percentage(exp, ctr):
    """Calculates the percentage change between an experimental value to a control value.
    = current / prior - 1"""
    if exp and ctr:
        return (1.*exp/ctr-1)*100


class Study(models.Model):
    """A lifespan study."""
    pmid = models.IntegerField(blank=True, null=True, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True, unique=True)
    link = models.URLField(blank=True, null=True)
    reference = models.ForeignKey(Reference, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    integrated = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    species = models.ManyToManyField('annotations.Species', blank=True)
    #experiments = models.OneToMany(Experiment) # ForeignKey?
    
    def __unicode__(self):
        if self.reference:
            return self.reference.__unicode__()
        else:
            return "{0} {1}".format(self.pmid, self.title)

    def get_absolute_url(self):
        return '/lifespan/study/%i' % self.pk

    class Meta():
        verbose_name_plural = "studies"

    def save(self, *args, **kwargs):
        """Check whether study is already in references and fetches annotation.
        1. Whether reference nor study exist.
        2. reference exist but not study.
        3. reference does not exit but study
        4. Both reference and study exist."""
        if self.title: kwargs['title'] = self.title
        if self.pmid: kwargs['pmid'] = self.pmid
        if self.link:
           kwargs['link'] = self.link
        if self.pmid: 
           reference, created = Reference.objects.get_or_create(pmid=self.pmid, defaults=kwargs)
           #print "models.Study.save() if self.pmid:", reference, created
           self.reference_was_created = created
        elif self.title:
           try:
               #print "TRRRRRRRRRRRRRRRYL reference, creating"
               try:
                   reference, created = Reference.objects.get_or_create(title__icontains=self.title, defaults=kwargs)
               except MultipleObjectsReturned as e:
                   references = Reference.objects.filter(title__icontains=self.title) #, defaults=kwargs)
                   for reference in references:
                       if reference.pmid:
                           break
                   created = False
               except Exception as e:
                   print e
               #print "TRRRRRRRRRRRRRRRYL reference, created", created
               #print reference, created
               self.reference_was_created = created
               #print "self.reference_was_created", self.reference_was_created
               self.reference = reference

               #print self.reference
               #super(Study, self).save()
               #print "Saved!"
               #print "Post save: ", self.reference
           except IntegrityError:
               return None
               #reference = Reference(**kwargs)
               #created = False
        else:
            reference = Reference(**kwargs)
            created = False

        #if not created and self.title:
           #reference.__dict__.update(#**kwargs)
           #reference.save()
           #print reference

        self.pmid = reference.pmid
        self.title = reference.title
        self.reference = reference
        try: super(Study, self).save()
        except IntegrityError as e:
            print e



class Experiment(models.Model):
    """A lifespan experiment composed of lifespan measurements.
    a.k.a. Measurements."""
    name = models.CharField(max_length=250, unique=True)
    data = models.TextField(blank=True, null=True)
    study = models.ForeignKey(Study)
    species = models.ForeignKey('annotations.Species')
    assay = models.ForeignKey('Assay', default=3)
    meta = {}

    keys = {'strain':['genotype'],
            'treatment':[],
            'mean':['mean lifespan (days)'],
            'max':['maximum lifespan (days)'],
            'pvalue':['p-values vs. control*', 'p', 'p-value'],
            'mean_extension':['mean lifespan change (days)'],
            'num': ['n'],
            'wild-type': ['wt', 'WT' 'wild type']
            }
    mapping = {}
    for k,v in keys.items():
        for i in v:
            mapping[i] = k

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u"lifespan/experiment/%s" % self.pk

    def save(self, *args, **kwargs):
        if self.pk:

            # Create a memory of the intervention mapping to a comparison:
            memory = {}
            comparisons = Comparison.objects.filter(exp__experiment=self)
            for comparison in comparisons:
                if  comparison.intervention:
                    memory[str(comparison)] = comparison.intervention

            # Eradicate all measurements and comparisons:
            measurements = Measurement.objects.filter(experiment=self)
            #print("Measurements: %s" % measurements)
            measurements.delete()

        else:
            memory = {}

        super(Experiment, self).save(*args, **kwargs)
        """Parses the associated data and creates the corresponding measurements."""
        data = self.data.replace('\r', '').replace(r'\\', '')
        if "#separator=" in data:
            separator = data.split('#separator=')[1].split('\n')[0]
        else:
            separator = ' '
        #if 'data' in kwargs:data = kwargs['data']
        data = data.split('\n')
        control = False

        header = data[0].lower().split(separator)
        for index, term in enumerate(header):
            if term in Experiment.mapping:
                header[index] = Experiment.mapping[term]
        #print(header)

        for line in data[1:]:
            #print(line)

            # Meta data text:
            if line.startswith('# '):
                continue

            # Meta data attributes:
            elif line.startswith('#'):
                #print("meta line %s" % line)
                attribute, value = line.split('#')[1].split('=')
                self.meta[attribute] = value
                continue

            # New experiment
            elif not line:
                control = False # Next line will be new control.
                continue

            # Actually data:
            columns = line.split(separator)
            measurement = Measurement(experiment = self)
            measurement.save()
            attributes = dict(zip(header, columns))
            for attr, value in attributes.items():
                #print(attr, value)
                #print self.meta
                if "background" in self.meta:
                    measurement.background, created = Strain.objects.get_or_create(name=self.meta['background'], species=self.species)
                if "temperature" in self.meta:
                    measurement.temperature = self.meta['temperature']
                if "gender" in self.meta:
                    #print("gender")
                    measurement.gender.add(Gender.objects.get(name=self.meta['gender']))
                    #print measurement.gender.all()
                if value: lower = value.lower()
                #print "attr, value:", attr, value
                value = examine(value)
                if attr in ['genotype', 'strain']:
                    # Separate strain from treatment:
                    if ";" in value and not "; ":
                        if "RNAi" in value:
                            strain = ';'.join(value.split(';')[:-1])
                            if lower in ['wt', 'wild type', 'wild-type']:
                                strain = multi_replace(strain, WT, 'wild-type')
                                measurement.genotype, created = Strain.objects.get_or_create(name=strain, species=self.species)
                            measurement.treatment = value.split(';')[-1]
                        else:
                            measurement.genotype, created = Strain.objects.get_or_create(name=value, species=self.species)
                    else:
                        #print(value)
                        if lower in ['wt', 'wild type', 'wild-type', 'canton-s', 'white1118']:
                            strain = multi_replace(value, WT, 'wild-type')
                            measurement.genotype, created = Strain.objects.get_or_create(name=strain, species=self.species)
                        else:
                            measurement.genotype, created = Strain.objects.get_or_create(name=value, species=self.species)
                if attr == "gender":
                    measurement.gender.add(Gender.objects.get(name=value))
                #elif attr =="pvalue":
                    #print value
                    #measurement.pvalue = unicode(value).replace("<", '')
                #elif attr.endswith("_extension"):
                elif attr == "treatment" and value:
                    if "(" in value:
                        gene, treatment = value.replace('(', '###').replace(')', '').split('###')
                        if not measurement.genotype:
                            measurement.genotype, created = Strain.objects.get_or_create(name=gene, species=self.species)
                        else:
                            measurement.diet = value
                            #measurement.genotype, created = Strain.objects.get_or_create(name=measurement.genotype.name+';'+gene, species=self.species)
                    else:
                        treatment = value
                    try:
                        measurement.manipulation = Manipulation.objects.get(shortcut=treatment)
                    except ObjectDoesNotExist:
                        measurement.manipulation = Manipulation.objects.get(name='mutation')
                else:
                    setattr(measurement, attr, value)

            #print("Attributes: %s" % attributes)
            if not control:
                control = measurement
                measurement.control = True
                measurement.save()
            else:
                measurement.save()
                comparison = Comparison()
                comparison.ctr = control
                comparison.exp = measurement
                comparison.pvalue = measurement.pvalue
                if "mean_extension" in attributes:
                    comparison.mean = attributes["mean_extension"]
                    #print("Measurement background = %s" % measurement.background)
                    #print("Mean extension %s" % comparison.mean)
                    comparison.ctr.genotype = measurement.background
                    comparison.ctr.save()
                    #print("Comparison ctr genotype: %s" % comparison.ctr.genotype)
                if "max_extension" in attributes:
                    comparison.max = attributes['max_extension']
                comparison.save()

                # Restore interventions mapping via memory:
                if str(comparison) in memory:
                    comparison.intervention = memory[str(comparison)]
                    comparison.save()


class Strain(models.Model):
    name = models.CharField(max_length=50)
    species = models.ForeignKey('annotations.Species')

    def __unicode__(self):
         return self.name

    def get_absolute_url(self):
        return u"/lifespan/strain/%s" % self.pk


class Measurement(models.Model):
    """A lifespan measurment from a table or graph."""
    experiment = models.ForeignKey(Experiment)
    comparisons = models.ManyToManyField("self", through="Comparison", symmetrical=False)
    control = models.BooleanField()

    background = models.ForeignKey(Strain, blank=True, null=True) # Genetic background.
    genotype = models.ForeignKey(Strain, blank=True, null=True, related_name='strain') #CharField(max_length=50, blank=True, null=True) # Wild-type or mutant.
    gender = models.ManyToManyField('Gender', blank=True, null=True)
    manipulation = models.ForeignKey('Manipulation', blank=True, null=True)
    diet = models.CharField(max_length=150, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    start = models.FloatField(blank=True, null=True) # Start age of treatment.

    # Lifespan measurement type:
    mean = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)   # Maximum lifespan
    num = models.IntegerField(blank=True, null=True)
    pvalue = None

    def __unicode__(self):
         return u"{0} {1}".format(self.genotype or '', self.diet or '')

    def get_absolute_url(self):
        return u"/lifespan/measurement/%s" % self.pk


class Epistasis(models.Model):
    """A possible enhancement of the restricted choices field."""
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
     
    def get_absolute_url(self):
        return u"/lifespan/epistasis/%s" % self.pk

    class Meta:
        verbose_name_plural = "epistases"


from annotations.mapping import mapid

class Comparison(models.Model):
    """A comparision between two lifespan measurements."""
    #EPISTATIC = (
    #    (1, _('Neutral')),
    #    (2, _('Addative')),
    #    (3, _('Multiplicative'))
    #           )
    exp = models.ForeignKey(Measurement, related_name="experimental_group")#, blank=True, null=True)
    ctr = models.ForeignKey(Measurement, related_name="control_group")#, blank=True, null=True)
    #epistasis = models.PositiveSmallIntegerField(max_length=1, blank=True, null=True, choices=EPISTATIC)
    epistasis = models.ForeignKey(Epistasis, blank=True, null=True)
    intervention = models.ForeignKey('Intervention', blank=True, null=True) # ManyToMany?
    #factors = models.ManyToManyField('Factor', blank=True, null=True)
    mean = models.FloatField(blank=True, null=True) # Mean lifespan extension.
    median = models.FloatField(blank=True, null=True) # Median lifespan extension.
    max = models.FloatField(blank=True, null=True) # Maximum lifespan extension.#
    pvalue = models.CharField(max_length=10, blank=True, null=True)#models.FloatField(blank=True, null=True)
    manipulation = 'dummy'

    def __unicode__(self):
        if self.exp.manipulation:
            manipulation = ' %s' % self.exp.manipulation.shortcut
        else:
            manipulation = ''
        return u"{0}{1} vs. {2}".format(self.exp.genotype, manipulation, self.ctr.genotype)

    def get_absolute_url(self):
        return u"/lifespan/comparison/%s" % self.pk

    @property
    def data(self):
        data = []
        attributes = [self.exp.manipulation, self.ctr.manipulation,
                      self.exp.background, self.ctr.background, self.exp.diet, self.ctr.diet,
                      #self.exp.gender.all(), self.ctr.gender.all(),
                      #self.exp.temperature, self.ctr.temperature,
                      round(self.mean or 0, 1), round(self.median or 0, 1), round(self.max or 0, 1), self.epistasis]
        for attribute in attributes:
            if attribute:
                data.append(attribute)
        return "; ".join(map(str, data))
        #return "; ".join([attribute for attribute in attributes if attribute])

    @property
    def exp_t(self):
        return self.exp.temperature

    @property
    def ctr_t(self):
        return self.ctr.temperature

    @property
    def t(self):
        if self.exp.temperature == self.ctr.temperature:
            return "%s°C" % int(self.exp.temperature)
        else:
            return "%s°C vs. %s°C" % (int(self.exp.temperature), int(self.ctr.temperature))

    @property
    def gender(self):
        exp_gender = ", ".join(gender.name for gender in self.exp.gender.all())
        ctr_gender = ", ".join(gender.name for gender in self.exp.gender.all())
        if exp_gender == ctr_gender:
            return exp_gender
        else:
            return "%s vs. %s" % (exp_gender, ctr_gender)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.mean = percentage(self.exp.mean, self.ctr.mean) or self.mean
            self.median = percentage(self.exp.median, self.ctr.median) or self.median
            self.max = percentage(self.exp.max, self.ctr.max) or self.max

            if self.exp.genotype:
                interventions = Intervention.objects.filter(name__icontains=self.exp.genotype)
            elif self.exp.diet:
                interventions = Intervention.objects.filter(name__icontains=self.exp.diet)
            else:
                interventions = []
                #Q(name__icontains=self.exp.genotype) | Q(name__icontains=self.ctr.genotype))
            #print("%s %s %s" % (self.exp.genotype, self.ctr.genotype, interventions))
            for intervention in interventions:
                self.intervention = intervention
            #print("mapping")
            if self.exp.genotype:
                if "/" in self.exp.genotype.name:
                    genotype = self.exp.genotype.name.split('/')[0]
                else:
                    genotype = self.exp.genotype.name
                if "(" in genotype:
                    genotype = genotype.split('(')[0].rstrip()
                #print("map id")
                #print(genotype)
                id = mapid(genotype, self.exp.experiment.species.taxid)
                #print("mapped")
            else:
                id = None
            if id:
                try:
                    factor = Factor.objects.get(entrez_gene_id=id)
                    interventions = factor.intervention.all()
                    if interventions:
                        self.intervention = interventions[0]
                except ObjectDoesNotExist:
                    pass # Make message
                    #print("ObjectDoesNotExist %s" % id)
                except MultipleObjectsReturned:
                    pass # Make message
                    #print("MultipleObjectsReturned %s" % id)

                    #print self.intervention
            #else: factor = ''
            #print("Mapped factor: %s = %s (%s) %s" % (genotype, id, factor, interventions))

        super(Comparison, self).save(*args, **kwargs)


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

    def get_absolute_url(self):
        return u"/lifespan/regimen/%s" % self.pk


class Assay(models.Model):
    name = models.CharField(max_length=40)
    shortcut = models.CharField(max_length=20)

    def __unicode__(self):
        return self.shortcut

    def get_absolute_url(self):
        return u"/lifespan/assay/%s" % self.pk


class Manipulation(models.Model):
    shortcut = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.ManyToManyField('self', symmetrical=False, related_name='type_of', blank=True)
    #type = models.ManyToManyField('self', through='ManipulationType', symmetrical=False, related_name='type_of', blank=True)

##    def add_manipulation_type(self, manipulation):
##        relationship
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u"/lifespan/manipulation/%s" % self.pk

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
    species = models.ForeignKey('annotations.Species', blank=True, null=True)
    sex = models.CharField(max_length=25, blank=True)
    gender = models.ManyToManyField('Gender', blank=True, null=True)
    background = models.CharField(max_length=250, blank=True)
    strain = models.ForeignKey('Strain', blank=True, null=True)
    effect = models.TextField(blank=True)
    mean = models.CharField(max_length=15, null=True, blank=True)
    median = models.CharField(max_length=15, null=True, blank=True)
    maximum = models.CharField(max_length=15, null=True, blank=True)
    _25 = models.CharField(max_length=15, null=True, blank=True)
    _75 = models.CharField(max_length=15, null=True, blank=True)
    manipulation = models.ManyToManyField(Manipulation, blank=True)
    pmid = models.CharField(max_length=250, blank=True)
    references = models.ManyToManyField('datasets.Reference', blank=True)
    lifespans = models.CharField(max_length=25, blank=True)
    
##    species = models.ManyToManyField(Species)
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/lifespan/intervention/%i" % self.pk

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.taxid and not self.species:
                self.species = Species.objects.get(taxid=self.taxid)
            elif not self.taxid and self.species:
                self.taxid = self.species.taxid
        super(Intervention, self).save(*args, **kwargs)


class Factor(models.Model):  # Rename to Entity AgeFactor
    entrez_gene_id = models.IntegerField("Entrez gene ID", null=True, blank=True)
    #geneid = models.ForeignKey(Gene, blank=True)   # Or Genes
    mapping = models.IntegerField(null=True, blank=True)
    ensembl_gene_id = models.CharField("Ensembl gene ID", max_length=18, blank=True)
    symbol = models.CharField(max_length=255, blank=True, help_text='In the case of genes providing the correct gene symbol and species name would be normally sufficient to identify a gene. ' #15
                'Other fields such as gene name and identifiers will be automatically populated.')   # Rename to symbol.
    name = models.CharField(max_length=244, blank=True)    # Rename to name.
    alias = models.CharField(max_length=270, blank=True)
    function = models.TextField(blank=True)    # Manually curated functional description field.
    description = models.TextField(blank=True) # Automatically populated field for functional descriptions.
    functional_description = models.TextField(blank=True)    
    observation = models.TextField(blank=True, help_text='Please provide references to the evidence why this factor was chosen to be classified. '
                                                         'In the ideal case provide a PMID in square brackets at the end of the sentence. '
                                                         'Multiple PMIDs can be separated by semicolon, e.g. "The gene XYZ was associated with aging in some way [12345; 67890].')
    classification = models.CharField(max_length=20, blank=True)
    classifications = models.ManyToManyField('annotations.Classification')
    regimen = models.ManyToManyField(Regimen, blank=True)
    assay = models.ManyToManyField(Assay, help_text='Choose the adequate lifespan, such as replicative (RLS), chronological (CLS) or organismal') # blank=True, null=True ?
    diet_regimen = models.CharField(max_length=250, blank=True)
    life_span = models.CharField("Tax ID", max_length=250, blank=True)
    taxid = models.IntegerField(null=True, blank=True, help_text="This field will be autofilled if you provide a species name")
    species = models.ForeignKey('annotations.Species', blank=True, null=True)
    pubmed_id = models.CharField("PubMed ID", max_length=250, blank=True)
    reference = models.CharField(max_length=250, blank=True)
    references = models.ManyToManyField('datasets.Reference', blank=True)
    mean = models.CharField(max_length=15, null=True, blank=True)
    median = models.CharField(max_length=15, null=True, blank=True)
    maximum = models.CharField(max_length=15, null=True, blank=True)
    _75 = models.CharField('75%ile', max_length=15, null=True, blank=True)
    _25 = models.CharField('25%lie', max_length=15, null=True, blank=True)
    manipulation = models.CharField(max_length=250, null=True, blank=True)
    intervention = models.ManyToManyField('Intervention', blank=True, related_name='factors')
    gene_intervention = models.CharField(max_length=250, null=True, blank=True)
    synergistic_epistasis = models.CharField(max_length=33, blank=True)
    antagonistic_epistasis = models.CharField(max_length=216, blank=True)
    human_homologue = models.CharField(max_length=18, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=25, null=True, blank=True) # Gene, or drug
    types = models.ManyToManyField(Type, blank=True)
    pdb = models.CharField(max_length=250, blank=True, null=True)
    #polymprhism


    def __unicode__(self):
        return self.symbol

    def get_absolute_url(self):
        return u"/lifespan/factor/%s" % self.pk

    def data(self):
        return self.entrez_gene_id, self.symbol, self.name, self.alias

    data = property(data)

    def save(self, *args, **kwargs):
        if not self.pk:
            if MAPPING:
                #print("lifespan.models.Factors.save()")
                if self.species:
                    self.taxid = taxid = self.species.taxid
                elif self.taxid:
                    taxid = self.taxid
                    self.species = Species.objects.get(taxid=taxid)
                else:
                    taxid = None
                ids = [self.entrez_gene_id, self.ensembl_gene_id, self.symbol, self.name]
                ids = m([str(id) for id in ids if id], taxid)
                entrez_gene_id = ids[0]
                if entrez_gene_id and isinstance(entrez_gene_id, int):
                    self.entrez_gene_id = self.entrez_gene_id or entrez_gene_id
                    if self.taxid == 4932:
                        self.ensembl_gene_id = ids[1]['ensembl_gene'] # ro maybe sgd
                        annotation = retrieve(self.ensembl_gene_id)
                        self.symbol = annotation['symbol']
                        self.name = annotation['name']
                        self.description = annotation['description']
                        if not self.function:
                            self.functional_description = self.description
                        if self.symbol and self.name:
                            number = re.findall('\d+', self.symbol) # match would be more suitable here.
                            if number:
                                self.name += " " + number[0]
                    else:
                        try:
                            entrez = Entrez.objects.get(entrez_gene_id=ids[0])
                            self.ensembl_gene_id = self.ensembl_gene_id or entrez.ensembl_gene_id
                            self.symbol = self.symbol or entrez.gene_symbol
                            self.name = self.name or entrez.gene_name
                        except ObjectDoesNotExist:
                            self.entrez_gene_id = ids[0]
                        if not self.taxid:
                            taxid = entrez.taxid
                            self.species = Species.objects.get(taxid=taxid)

        super(Factor, self).save(*args, **kwargs)


class State(models.Model):
    name = models.CharField(max_length=250)

    objects = StateManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('state', args=[self.pk])


class Technology(models.Model): # PCR, array
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('technology', args=[self.pk])

    class Meta:
        verbose_name_plural = 'Technologies'


class StudyType(models.Model): # GWAS, Candidate genes
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('study_type', args=[self.pk])

from mptt.models import MPTTModel, TreeForeignKey




# Classifications Ontology:

class Population(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('population', args=[self.pk])

    class MPTTMeta:
        order_insertion_by = ['name']

# class Association(models.Model):
#     def __unicode__(self):
#         return self.polymorphism


class VariantType(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Variant Type'
        verbose_name_plural = 'Variant Types'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('variant_type', args=[self.pk])


class ORType(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Odds ratio Type'
        verbose_name_plural = 'Odds ratio Types'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('or_type', args=[self.pk])


class Variant(models.Model):

    CHOICES = (
        (1, _('Positive')),
        (2, _('Negative')),
    #    (3, _('Multiplicative'))
               )

    finding = models.PositiveSmallIntegerField(max_length=1, blank=True, null=True, choices=CHOICES,
                                               help_text="Whether finding was positive or negative.")
    #polymorphism = models.CharField(max_length=20)# genetic variant
    created = models.DateTimeField(_('created'), auto_now_add=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    location  = models.CharField(max_length=10, null=True, blank=True)# genomic location
    factor = models.ForeignKey(Factor, null=True, blank=True)
    shorter_lived_allele = models.CharField(max_length=255, blank=True, null=True)
    longer_lived_allele = models.CharField(max_length=255, blank=True, null=True)
    variant_type = models.ForeignKey('VariantType', blank=True, null=True)
    or_type = models.ForeignKey('ORType', help_text='Odds Ratio Type', blank=True, null=True)


    polymorphism = models.CharField(max_length=255)# genetic variant
    alias = models.CharField(max_length=255, blank=True, null=True,
                             help_text='Individual alias names should be seperated by semicolon ";"')
    #variants = models.ManyToManyField(Variant)
    factors = models.ManyToManyField(Factor, null=True, blank=True, related_name='variances')
    description = models.TextField(null=True, blank=True)
    odds_ratio = models.FloatField(null=True, blank=True)
    pvalue = models.FloatField(null=True, blank=True, help_text="Numerical value of the p-value")
    p_value = models.CharField(max_length=255, null=True, blank=True, help_text="String representation of the p-value, e.g. > 0.05 (females)")# genetic variant
    qvalue = models.FloatField(null=True, blank=True)
    significant = models.CharField(max_length=255, null=True, blank=True)  # (redudant)
    initial_number = models.CharField(max_length=250, null=True, blank=True) # _of_cases_controls (study)
    replication_number = models.CharField(max_length=250, null=True, blank=True) #     _of_cases_controls (study)
    ethnicity = models.ManyToManyField(Population)# German
    age_of_cases = models.CharField(max_length=250, null=True, blank=True)
    study_type = models.ForeignKey(StudyType, null=True, blank=True)    # GWAS, Candidate genes
    technology = models.ForeignKey(Technology, null=True, blank=True)     # PCR, array
    pmid = models.IntegerField(blank=True, null=True)
    reference = models.ForeignKey('datasets.Reference')
    choice = models.ForeignKey(State, default=1, null=True, blank=True) #[Curate/Review/Discard]
    classifications = models.ManyToManyField('annotations.Classification', blank=True, null=True, default=None)

    objects = VariantManager()

    def __unicode__(self):
        return self.polymorphism

    def get_absolute_url(self):
        return reverse('variant', args=[self.pk])







class Gender(models.Model):
    name = models.CharField(max_length=13)

    def __unicode__(self):
        return self.name

m2m_changed.connect(handlers.changed_references, sender=Intervention.references.through)
m2m_changed.connect(handlers.changed_references, sender=Factor.references.through)