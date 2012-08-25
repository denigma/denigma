"""Gene regulatory module."""
from django.db import models

#from omics import Chromosome, Gene (annotations)


class Match(models.Model):
    """A match of a sequence motif in the genome."""
    sequence = models.CharField(max_length=250) # String representation of the base sequence.
    chrom = models.CharField(max_length=10) # Chromosome.
    # chrom = models.ForeignKey(Chromosome)
    strand = models.BooleanField() # Orientation.
    start = models.IntegerField() # Chromosomal start coordinate.
    stop = models.IntegerField() # Chromosomal stop/end coordinate.


class Motif(models.Model):
    """A consensus motif which has multiple matches in the genome."""
    pattern = models.CharField(max_length=250) # Consensus sequence.
    matches = models.OneToManyField(Match) # Sequence matches.


class Factor(models.Model):
     """A transcription factor that can have mutliple motifs associated to it."""
     name = models.CharField(max_length=50) # Primary name of the factor
     motifs = models.ManyToManyField(Motif)
     # gene = models.ForeignKey(Gene)



    


