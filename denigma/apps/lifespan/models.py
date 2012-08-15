from django.db import models
from annotation.models import Reference, Intervention


class Study(models.Model):
    """A lifespan study."""
    pmid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    reference = models.ForeignKey(Reference)
    experiments = models.OneToMany(Experiment) # ForeignKey?


class Experiment(models.Model):
    """A lifespan experiment."""
    data = models.TextField(blank=True, blank=True)


class Measurment(models.Model):
    """A lifespan measurment from a table or graph."""
    data =
    comparision = ManyToManyField(self, through="Comparision")
    control = BooleanField()


class Comparision(models.Model):
    """A comparision between two lifespan measurements."""
    EPISTATIC =(
        (1, (_'Additive')),
        (2, (_'Neutral')),
        (3, (_'Multiplicative')),)
    experimental = model.ForeignKey(Measurment)
    control = models.ForeignKey(Measurment)
    epistasis = models.PositiveSmallIntegerField(max_lengh=1, choices=EPISTATIC)#models.ForeignKey(Epistasis)
    intervention = models.ForeignKey(Intervention) # ManyToMany?


class Epistasis(models.Model):
    """A possible enhancment of the restricted choices field."""
    name = models.CharField(max_length=20)
    
    
    
    
