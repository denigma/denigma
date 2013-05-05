from django.db import models


class Analysis(models.Model):
    """A network analysis."""
    name = models.CharField(max_length=250)
    taxid = models.IntegerField()
    species = models.ForeignKey('annotations.Species')

    class Meta:
        verbose_name_plural = 'Analyses'

    def __unicode__(self):
        return self.name


class Enrichment(models.Model):
    """Functional enrichment."""
    term = models.CharField(max_length=250)
    t = models.IntegerField()
    s = models.IntegerField()
    r = models.FloatField()
    pvalue = models.FloatField()
    genes = models.TextField()
    analysis = models.ForeignKey(Analysis)

    def __unicode__(self):
        return self.term


class Candidate(models.Model):
    entrez_gene_id = models.IntegerField()
    gene_symbol = models.CharField(max_length=40, blank=True)
    gene_name = models.TextField(blank=True)
    t = models.IntegerField()
    s = models.IntegerField()
    specificity =  models.FloatField(null=True, blank=True)
    p_value = models.FloatField(db_column='p-Value', null=True, blank=True)
    taxid = models.IntegerField()
    species = models.ForeignKey('annotations.Species', blank=True, null=True)
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
    analysis = models.ForeignKey(Analysis)
#
#      class Meta:
#           db_table = u'Candidate' # Rename and move to datasets_candidates?