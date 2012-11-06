# -*- coding: utf-8 -*-
import re

from django.db import models, IntegrityError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import m2m_changed

from datasets.models import Reference

try:
    from annotations.mapping import m
    from annotations.models import Entrez, Species
    MAPPING = True
except:
    MAPPING = False

import handlers


WT = ['wt', 'WT' 'wild type']


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
           print "models.Study.save() if self.pmid:", reference, created
           self.reference_was_created = created
        elif self.title:
           try:
               print "TRRRRRRRRRRRRRRRYL reference, creating"
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
               print "TRRRRRRRRRRRRRRRYL reference, created", created
               print reference, created
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
    #assay = models.ForeignKey('Assay')
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
            # Eradicate all measurements and comparisons:
            measurements = Measurement.objects.filter(experiment=self)
            print("Measurements: %s" % measurements)
            measurements.delete()
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
        print(header)

        for line in data[2:]:
            #print line

            # Meta data text:
            if line.startswith('# '):
                continue

            # Meta data attributes:
            elif line.startswith('#'):
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
            for attr, value in dict(zip(header, columns)).items():
                if "background" in self.meta:
                    measurement.background = Strain.objects.get_or_create(name=self.meta['background'])
                if value: lower = value.lower()
                #print "attr, value:", attr, value
                value = examine(value)
                if attr in ['genotype', 'strain']:
                    # Separate strain from treatment:
                    if ";" in value:
                        if "RNAi" in value:
                            strain = ';'.join(value.split(';')[:-1])
                            if lower in ['wt', 'wild type', 'wild-type']:
                                strain = multi_replace(strain, WT, 'wild-type')
                                measurement.genotype, created = Strain.objects.get_or_create(name=strain)
                            measurement.treatment = value.split(';')[-1]
                        else:
                            measurement.genotype, created = Strain.objects.get_or_create(name=value)
                    else:
                        print value
                        if lower in ['wt', 'wild type', 'wild-type', 'canton-s', 'white1118']:
                            strain = multi_replace(value, WT, 'wild-type')
                            measurement.genotype, created = Strain.objects.get_or_create(name=strain)
                        else:
                            measurement.genotype, created = Strain.objects.get_or_create(name=value, species=self.species)
                if attr.lower() == "gender":
                    measurement.gender.add(Gender.objects.get(name=value.lower()))
                else:
                    setattr(measurement, attr, value)
            if not control:
                control = measurement
                measurement.control = True
                measurement.save()
            else:
                measurement.save()
                comparision = Comparision()
                comparision.ctr = control
                comparision.exp = measurement
                comparision.save()



class Strain(models.Model):
    name = models.CharField(max_length=25)
    species = models.ForeignKey('annotations.Species')

    def __unicode__(self):
         return self.name

    def get_absolute_url(self):
        return u"/lifespan/strain/%s" % self.pk


class Measurement(models.Model):
    """A lifespan measurment from a table or graph."""
    experiment = models.ForeignKey(Experiment)
    comparisions = models.ManyToManyField("self", through="Comparision", symmetrical=False)
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


class Comparision(models.Model):
    """A comparision between two lifespan measurements."""
    #EPISTATIC = (
    #    (1, _('Neutral')),
    #    (2, _('Addative')),
    #    (3, _('Multiplicative'))
    #           )
    exp = models.ForeignKey(Measurement, related_name="experimental_group")
    ctr = models.ForeignKey(Measurement, related_name="control_group")
    #epistasis = models.PositiveSmallIntegerField(max_length=1, blank=True, null=True, choices=EPISTATIC)
    epistasis = models.ForeignKey(Epistasis, blank=True, null=True)
    intervention = models.ForeignKey('Intervention', blank=True, null=True) # ManyToMany?
    #factors = models.ManyToManyField('Factor', blank=True, null=True)
    mean = models.FloatField(blank=True, null=True) # Mean lifespan extension.
    median = models.FloatField(blank=True, null=True) # Median lifespan extension.
    max = models.FloatField(blank=True, null=True) # Maximum lifespan extension.#

    def __unicode__(self):
        return u"{0} vs. {1}".format(self.exp.genotype, self.ctr.genotype)

    def get_absolute_url(self):
        return u"/lifespan/comparision/%s" % self.pk

    @property
    def data(self):
        data = []
        attributes = [self.exp.manipulation, self.ctr.manipulation,
                      self.exp.background, self.ctr.background, self.exp.diet, self.ctr.diet,
                      self.mean, self.median, self.max, self.epistasis]
        for attribute in attributes:
            if attribute:
                data.append(attribute)
        return "; ".join(map(str, data))
        #return "; ".join([attribute for attribute in attributes if attribute])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.mean = percentage(self.exp.mean, self.ctr.mean)
            self.median = percentage(self.exp.median, self.ctr.median)
            self.max = percentage(self.exp.max, self.ctr.max)

            interventions = Intervention.objects.filter(
                Q(name__icontains=self.exp.genotype) | Q(name__icontains=self.ctr.genotype))
            #print("%s %s %s" % (self.exp.genotype, self.ctr.genotype, interventions))
            for intervention in interventions:
                self.intervention = intervention
            #factor = mapping(exp.genotype, exp.experiment.species.taxid)

        super(Comparision, self).save(*args, **kwargs)


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
    life_span = models.CharField("Tax ID", max_length=250, blank=True)
    taxid = models.IntegerField(null=True, blank=True)
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
                    entrez = Entrez.objects.get(entrez_gene_id=ids[0])
                    self.entrez_gene_id = self.entrez_gene_id or entrez_gene_id
                    self.ensembl_gene_id = self.ensembl_gene_id or entrez.ensembl_gene_id
                    self.symbol = self.symbol or entrez.gene_symbol
                    self.name = self.name or entrez.gene_name
                    if not self.taxid:
                        taxid = entrez.taxid
                        self.species = Species.objects.get(taxid=taxid)

        super(Factor, self).save(*args, **kwargs)


class Gender(models.Model):
    name = models.CharField(max_length=13)

    def __unicode__(self):
        return self.name

m2m_changed.connect(handlers.changed_references, sender=Intervention.references.through)
m2m_changed.connect(handlers.changed_references, sender=Factor.references.through)