# -*- coding: utf-8 -*-
from time import strptime
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models

from Bio import Entrez, Medline



Entrez.email = "hevok@denigma.de"


# Helper function
def normalize_time(date):
    """Normalizes time attributes for storing into DateTimeField."""
    try:
        time = datetime(*strptime(date, "%Y/%m/%d %H:%M")[0:5])
    except:
        try:
            time = datetime(*strptime(date, "%Y/%m/%d")[0:3])
        except:
            try:
                time = datetime(*strptime(date, "%Y-%m-%d")[0:3])
            except:
                months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'Mai':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10,'Nov':11, 'Dec':12}
                for month, number in months.items():
                    if month in date:
                        date = date.replace(month, unicode(number))
                try:
                    time = datetime(*strptime(date, "%Y %m %d")[0:3])
                except:
                    try:
                        time = datetime(*strptime(date, "%Y %m")[0:3])
                    except:
                        time = datetime(*strptime(date, "%Y")[0:3])
    return time



def normalize_title(title):
    title = title.lower()
    if title.endswith('.'):
        title = title[:-1]
    return title


class Reference(models.Model):
    pmid = models.IntegerField(blank=True, null=True, unique=True) #) # 
    title = models.CharField(max_length=400, blank=True)
    authors = models.TextField(blank=True)  #models.ManyToManyField(Author) max_length=250, 
    abstract = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True) #CharField(max_length=250, blank=True) #
    link = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    journal = models.CharField(max_length=250, blank=True)
    year = models.IntegerField(blank=True, null=True)
    volume = models.CharField(max_length=20, blank=True, null=True)
    issue = models.CharField(max_length=10, blank=True, null=True) # Was Integer, but encounterd "2-3" value!
    pages = models.CharField(max_length=23, blank=True)
    start_page = models.IntegerField(blank=True, null=True)
    epub_date = models.DateField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type_of_article = models.CharField(max_length=10, blank=True, null=True)
    short_title = models.CharField(max_length=50, blank=True, null=True)
    alternate_journal = models.CharField(max_length=150, blank=True, null=True)
    issn = models.IntegerField(blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    original_publication = models.CharField(max_length=100, blank=True)
    reprint_edition = models.CharField(max_length=100, blank=True, null=True)
    reviewed_items = models.CharField(max_length=100, blank=True, null=True)
    legal_note = models.CharField(max_length=100, blank=True, null=True)
    pmcid = models.IntegerField(blank=True, null=True)
    nihmsid = models.IntegerField(blank=True, null=True)
    article_number = models.IntegerField(blank=True, null=True)
    accession_number = models.IntegerField(blank=True, null=True)
    call_number = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=100, blank=True, null=True)    # Make it to a ManyToManyField.
    research_notes = models.CharField(max_length=100, blank=True, null=True) # dito.
    #file_attachment = models.FileField(blank=True)
    author_address = models.CharField(max_length=150, blank=True, null=True)
    #figure = models.ImageField(blank=True)
    caption = models.CharField(max_length=100, blank=True, null=True)
    access_date = models.DateField(blank=True, null=True)
    translated_author = models.CharField(max_length=100, blank=True, null=True)
    name_of_database = models.CharField(max_length=100, blank=True, null=True)
    database_provider = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=75, blank=True, null=True)        

    def __unicode__(self):
        return u"{0} {1}".format(self.pmid, self.title)

    def get_absolute_url(self):
        return reverse('detail-reference', args=[self.pk])

    def save(self, update=False, *args, **kwargs):
        if not self.pk or update:
            # This code only happens if the objects is not in the database yet.
            # Otherwise it would have pk.
            try:
                #Reference._for_write = True
                if self.pmid or 'pmid' in kwargs:
                    print "Did not failed"
                    return Reference.objects.get(pmid=self.pmid) #, False
                elif self.title or 'title' in kwargs:
                    #print self.title
                    handle = Entrez.esearch(db='pubmed', term=self.title)
                    print "Got handle"
                    record = Entrez.read(handle)
                    print "Got record", record
                    print record['Count'], type(record['Count'])
                    if record['Count'] == "1":
                       print "Record count is 1"
                       self.pmid = record['IdList'][0]
                       #print self.title, self.pmid
                       Reference.fetch_data(self)
                       print("Saving")
                       super(Reference, self).save(*args, **kwargs)
                       print("Saved")
                    else:
                       from denigma.library import Bibliography # This statement at the top breaks Denigma for unknown reason.
                       #print("Trying it different. %s" % type(self.title))
                        # Google:
                       bib = Bibliography()
                       #print("googling")
                       r = bib.google(self.title)
                       if r:
                           r = r[0]
                           self.pmid = r.pmid
                           #print("Google successufull: %s" % self.pmid)
                       else:
                           #print("Google failed.")
#                           r = bib.find(self.title)[0]
#                           self.pmid = r.pmid
#                           print self.pmid
                           #print("Trying it different.")
                           r = bib.find(unicode(self.title))
                           if len(r) == 1:
                               r = r[0]
                               self.pmid = r.pmid
                               print self.pmid
                           elif len(r) > 1:
                               title = normalize_title(self.title)
                               for areference in r:
                                   if normalize_title(areference.title) == title:
                                       r = areference
                       print("datasets.Reference.save()")
                       self.__dict__.update(r.__dict__)
                       print r
                       print vars(r)
                       self.date = normalize_time(r.date)

                       print "# Transforming lists into strings:"
                       self.keywords = "; ".join(self.keywords)
                       self.authors = "; ".join(self.authors)
                       print "calling super"
                       print self.pmid
                       try: super(Reference, self).save(*args, **kwargs) # Just save the given information.
                       except Exception as e:
                           print e
                       print "called super"
                       # Raise Exception and state the the given information yielded more than one reference.
                else:
                    super(Reference, self).save(*args, **kwargs)
            except Reference.DoesNotExist as e:
                print "Error", e
                Reference.fetch_data(self)
                super(Reference, self).save(*args, **kwargs)
        else:
            super(Reference, self).save(*args, **kwargs)

    @staticmethod
    def fetch_data(self):
        """Queries Entrez EUtils to retrieve information on a reference."""
        if self.pmid:
          try:
            handle = Entrez.esummary(db="pubmed", id=self.pmid)
            r = Entrez.read(handle)
            # print r
            r = r[0] #  reference.
            self.title = unicode(r['Title'])
            self.volume = r.get('Volume', None) or None
            self.issue = r.get('Issue', None) or None
            self.pages = r['Pages']
            self.authors = unicode('; '.join(r['AuthorList']))
            self.journal = r['FullJournalName']
            self.alternate_journal = r['Source']
            self.year = int(r['PubDate'].split(' ')[0])
            self.language = r['LangList'][0]
            self.doi = r.get('DOI', None)

            handle = Entrez.efetch(db="pubmed", id=self.pmid, rettype="medline", retmode="text")
            records = Medline.parse(handle)
            for record in records: pass
            self.abstract = record.get('AB', None)
            s = record['EDAT']
            #print "; ".join(record.get('MH', ''))
            self.keywords = "; ".join(record.get('MH', '')) or None # MeSH terms
          except Exception as e:
               print "Failed fetching information"
               print e, self
          if not self.title:
            from denigma.library import Bibliography
            bib = Bibliography()
            r = bib.efetch(id=self.pmid)
            #print("datasets.Reference.fetch_data")
            self.__dict__.update(r.__dict__)

            # Transforming lists into strings:
            self.keywords = "; ".join(self.keywords)
            self.authors = "; ".join(self.authors)

          self.date = normalize_time(s)

    @property
    def info(self):
        r = self
        return "Title: %s\n Volume: %s\n Issue: %s\n Pages: %s\n Authors: %s\n Journal: %s\n Alternate_journal: %s\n Year: %s\n Language: %s\n DOI: %s\n Abstract: %s\n Date: %s\n Keywords: %s\n"\
               % (r.title, r.volume, r.issue, r.pages, r.authors,r.journal, r.alternate_journal, r.year, r.language, r.doi, r.abstract, r.date, r.keywords) 

    @staticmethod
    def update():
       """Updates all reference that have a pmid with information from Entrez."""
       references = Reference.objects.all()
       for reference in references:
           Reference.fetch_data(reference)
           try:
               reference.save()
           except Exception as e:
               print e
               #print reference.info, type(reference.volume), type(reference.issue), type(reference.pages)

    @staticmethod
    def duplicates():
       """Returns all duplicate entries.
       For now it checks only pmids."""
       references = Reference.objects.all() 
       pmids = {}
       duplicates = []
       for reference in references:
           if reference.pmid:
               if reference.pmid in pmids:
                   duplicates.extend([reference, pmids[reference.pmid]])
               else:
                   pmids[reference.pmid] = reference
       return duplicates

    @staticmethod
    def remove_dotes():
        """Removes the ending dots from all reference titles."""
        references = Reference.objects.all()
        for reference in references:
            if reference.title.endswith('.'):
                reference.title = reference.title[:-1]
                reference.save()

    @staticmethod
    def add_dots():
        """Appends dot to the title if not present."""
        references = Reference.objects.all()
        for reference in references:
            if not reference.title.endswith('.'):
                reference.title = reference.title + "."
                reference.save()


    def __repr__(self):
        if self.authors and self.title:
            authors = self.authors.split('; ')
            representation = self.repr()
            return "%s %s" % (representation, self.title)
        elif self.title:
            return self.title
        else:
            return u'{0}'.format(self.pmid)

    def repr(self, full=True):
        """Implement au field for short author names."""
        if full:
            authors = self.authors.split('; ')
        else:
            authors = self.au.split('; ')
        if len(authors) == 1:
            representation = "%s, %s" % (authors[0], self.year)
        elif len(authors) == 2:
            representation = "%s & %s, %s" % (authors[0], authors[1], self.year)
        else:
            representation = "%s et al., %s" %(authors[0], self.year)
        return representation

    def ref(self):
        if self.volume and self.pages:
            return "%s (%s) *%s* %s %s: %s." % (self.authors.replace(';', ','), self.year, self.title, self.journal, self.volume, self.pages)
        else:
            return "%s (%s) *%s* %s." % (self.authors.replace(';', ','), self.year, self.title, self.journal)

    @property
    def citations(self):
        return ref()

class Signature(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    symbol = models.CharField(max_length=30, blank=True)
    exp = models.FloatField(blank=True)
    ctr = models.FloatField(blank=True)
    fold_change = models.FloatField(blank=True)
    p_value = models.FloatField(blank=True)
    experimental = models.CharField(max_length=30, blank=True)
    control = models.CharField(max_length=30, blank=True)
    tissue = models.CharField(max_length=30, blank=True)
    age = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.symbol


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __unicode__(self):
        return u'%s %s' % (self.first.name, self.last_name)


class Gendr(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    ensembl_gene_id = models.CharField(max_length=18, blank=True)
    gene_symbol = models.CharField(max_length=13, blank=True)
    gene_name = models.CharField(max_length=150, blank=True)
    alias = models.CharField(max_length=50, blank=True)
    function = models.CharField(max_length=500, blank=True)
    observation = models.TextField(blank=True)
    classification = models.CharField(max_length=10)
    regimen = models.ManyToManyField('lifespan.Regimen')
    lifespan = models.ManyToManyField('lifespan.Assay')
    taxid = models.IntegerField()
    pubmed_id = models.CharField(max_length=87, blank=True)
    reference = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.gene_symbol
##    def get_fields(self):
##        #make a list of field/values.
##        return [(field, field.value_to_string(self)) for field in Gendr._meta.fields]
    @property
    def lifespans(self):
        return Lifespan.objects.filter(gendr__lifespan=self).all()

    class Meta:
       verbose_name = u"GenDR"
       verbose_name_plural = u"GenDR"


class Change(models.Model):
    name = models.CharField(max_length=250)
    taxid = models.IntegerField(null=True, blank=True)
    reference = models.CharField(max_length=250, null=True, blank=True)
    pmid = models.IntegerField(null=True, blank=True)
    tissue = models.CharField(max_length=250, null=True, blank=True)
    comparision = models.CharField(max_length=250, null=True, blank=True)
    start = models.CharField(max_length=250, null=True, blank=True)
    stop = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=25, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    description = models.TextField(max_length=250, blank=True)

    def __repr__(self):
        return self.name

    class Meta():
        verbose_name = u"Biological change"
        verbose_name_plural = u"Biological changes"


class GenCC(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=13, blank=True)
    alias = models.CharField(max_length=68, blank=True)
    taxid = models.IntegerField()
    function = models.CharField(max_length=255, blank=True)
    observation = models.CharField(max_length=248, blank=True)
    pubmed_id = models.IntegerField(null=True, blank=True)
    reference = models.CharField(max_length=37, blank=True)
    classification = models.CharField(max_length=5)
    peak_mrna = models.CharField(max_length=5, blank=True)
    peak_protein = models.CharField(max_length=5, blank=True)
    peak_actvity = models.CharField(max_length=5, blank=True)
    procession = """
    Identified entrez_gene_id 22339 for gene_symbol Vegf via Alias alias.
    Pp2a mapped to multiple genes via Alias alias.
    """  

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = u"GenCC"
       verbose_name_plural = u"GenCC"


class AdultHeightAssociation(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    locus_rank = models.IntegerField()
    chr = models.CharField(max_length=5)
    gene_symbol = models.CharField(max_length=8)
    snp = models.CharField(max_length=10)
    effect_allele = models.CharField(max_length=1)
    male_effect = models.CharField(max_length=1)
    male_p = models.FloatField()
    female_effect = models.CharField(max_length=1)
    female_p = models.FloatField()
    phet_m_vs_f = models.FloatField()
    taxid = 9606

    def __unicode__(self):
        return self.gene_symbol


class CircadianSystemicEntrainedFactors(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=13)
    alias = models.CharField(max_length=13, blank=True)
    taxid = 10090
    classification = 'CS'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name_plural = u"Circadian systemic entrained factors"


class ClockModulator(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    confirmed_by_bmal1_kockdown = models.CharField(max_length=10)
    gene_symbol = models.CharField(max_length=9)
    rna_nucleotide_accession_version = models.CharField(max_length=12)
    gene_name = models.CharField(max_length=152)
    phenotype = models.CharField(max_length=30)
    classification = models.CharField(max_length=8)
    taxid = 9606
    processing = '''
    14.01.2011 Converted Disconected Ids to current_entrez_gene_ids via mapping10.py:
    Changed Gene CDC2L1 in Dataset Zhang2009 from 442766 to 984
    Changed Gene CMYA4 in Dataset Zhang2009 from 191583 to 146862
    Changed Gene HRPT2 in Dataset Zhang2009 from 3279 to 79577
    Changed Gene ZNF261 in Dataset Zhang2009 from 442790 to 9203
    Changed Gene WDR9 in Dataset Zhang2009 from 379039 to 54014
    22.01.2011 41 of 394 genes were not mapped to entrez gene id and 2 mapped to multiple
    secondary mapping left 6 genes as unmapped
    Mannually mapping:
    Record removed. NM_182831.1: This RefSeq was permanently suppressed because currently there is support for the transcript but not for the protein.
    --> gene_symbol = 'C16orf82' --> entrez_gene_id = 162083; alias = 'TNT'; other = "Protein TNT"

    NM_020755 --> entrez_gene_id = 57515; alias = 'TDE2'; other_designation = 'tumor differentially expressed 2'    


    used Rna nucleotide accession version with __startwith clausal to map the remaining 4
    '''

    def __unicode__(self):
       return self.gene_symbol

    
class HumanGenes(models.Model):
    mapping = models.IntegerField(null=True, blank=True)
    hagrid = models.IntegerField()
    gene_symbol = models.CharField(max_length=8)
    gene_name = models.CharField(max_length=131)
    aliases = models.CharField(max_length=68, blank=True)
    epd_accession = models.CharField(max_length=11, blank=True)
    orf_accession = models.CharField(max_length=12)
    cds_accession = models.CharField(max_length=12, blank=True)
    selection_reason = models.CharField(max_length=21)
    band = models.CharField(max_length=10)
    location_start = models.IntegerField()
    location_end = models.IntegerField()
    orientation = models.IntegerField()
    function = models.CharField(max_length=94)
    cellular_location = models.CharField(max_length=40)
    expression = models.CharField(max_length=69)
    observations = models.TextField()
    omim = models.IntegerField()
    hprd = models.IntegerField()
    unigene = models.IntegerField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    homologene = models.IntegerField()
    swiss_prot = models.CharField(max_length=11, blank=True)
    interactions = models.TextField(blank=True)
    homologues = models.TextField()
    reference = models.TextField()
    pubmed_ids = models.TextField()
    taxid = 9606
    classification = 'AA'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = u"Human gene"


class JoanneGenes(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=8)
    ensembl_gene_id = models.CharField(max_length=16)
    dn = models.FloatField()
    ds = models.FloatField()
    dn_ds = models.FloatField()
    human_percentage_id = models.IntegerField()
    chimp_percentage_id = models.IntegerField()
    chimp_ensembl_gene_id = models.CharField(max_length=19)
    assoc_gene_name = models.CharField(max_length=8)
    cds_length = models.IntegerField()
    longevity = models.CharField(max_length=18)
    taxid = 9606
    classification = 'LA'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name_plural = u"Joanne genes"


class MurineImprinted(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=9)
    chromosome = models.CharField(max_length=4)
    chromosome_region = models.CharField(max_length=7)
    expressed_parental_allele = models.CharField(max_length=1)
    gene_name = models.CharField(max_length=74)
    classification = models.CharField(max_length=5)
    taxid = 10090

    def __unicode__(self):
       return self.symbol

    class Meta:
       verbose_name = u"murine imprinted gene"


class NewLongevityRegulators(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    wormbase_id = models.CharField(max_length=14)
    phenotype = models.CharField(max_length=11)
    classification = models.CharField(max_length=2)
    taxid = 6239

    def __unicode__(self):
        return self.wormbase_id

    class Meta:
        verbose_name = u"new longevity regulator"


class NewLongevityRegulatorsCandidates(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    wormbase_id = models.CharField(max_length=14, blank=True)
    gene_symbol = models.CharField(max_length=9, blank=True)
    ensembl_gene_id = models.CharField(max_length=11)
    taxid = 6239

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = u"new longevity regulator candidate"


class SurvivingInTheCold(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    locus_tag = models.CharField(max_length=10)
    protein_accession_number = models.CharField(max_length=10)
    sgd_id = models.CharField(max_length=10)
    embl = models.CharField(max_length=6)
    taxid = 4932
    classification = 'PG'

    def __unicode__(self):
        return self.locus_tag

    class Meta:
        verbose_name_plural = u"surviving in the cold"


class HumanBrainDnaMethylationChanges(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=10)
    chr = models.IntegerField()
    genomic_position_in_bp = models.IntegerField()
    gene_symbol = models.CharField(max_length=7)
    distance_to_tss = models.IntegerField()
    stage_i_pvalue_crblm = models.FloatField()
    stage_i_pvalue_fctx = models.FloatField()
    stage_i_pvalue_pons = models.FloatField()
    stage_i_pvalue_tctx = models.FloatField()
    stage_ii_pvalue_crblm = models.FloatField()
    stage_ii_pvalue_fctx = models.FloatField()
    beta_coefficient_range = models.CharField(max_length=13)
    adjusted_r2_estimates_from_stage_i_crblm = models.FloatField()
    adjusted_r2_estimates_from_stage_i_fctx = models.FloatField()
    adjusted_r2_estimates_from_stage_i_pons = models.FloatField()
    adjusted_r2_estimates_from_stage_i_tctx = models.FloatField()
    cpg_sequence = models.TextField(blank=True)
    size = models.CharField(max_length=4)
    cpg_count = models.CharField(max_length=4)
    c_g_count = models.CharField(max_length=4)
    percentage_cpg = models.CharField(max_length=4)
    percentage_c_or_g = models.CharField(max_length=4)
    ratio = models.CharField(max_length=4)
    cpg_sequence_2kb = models.TextField(blank=True)
    taxid = 9606
    classification = 'AM'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = u"human brain DNA methylation change"


class HumanBrainMethylationChanges(models.Model):
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=10)
    chr = models.IntegerField()
    genomic_position_in_bp = models.IntegerField()
    symbol = models.CharField(max_length=8)
    distance_to_tss = models.IntegerField()
    stage_i_p_value_crblm = models.FloatField()
    stage_i_p_value_fctx = models.FloatField()
    stage_i_p_value_pons = models.FloatField()
    stage_i_p_value_tctx = models.FloatField()
    stage_ii_p_value_crblm = models.FloatField()
    stage_ii_p_value_fctx = models.FloatField()
    beta_coefficient_range = models.CharField(max_length=24)
    adjusted_r2_estimates_from_stage_i_crblm = models.FloatField()
    adjusted_r2_estimates_from_stage_i_fctx = models.FloatField()
    adjusted_r2_estimates_from_stage_i_pons = models.FloatField()
    adjusted_r2_estimates_from_stage_i_tctx = models.FloatField()
    cpg_sequence = models.TextField(blank=True)
    size = models.CharField(max_length=4)
    cpg_count = models.CharField(max_length=4)
    c_g_count = models.CharField(max_length=4)
    percentage_cpg = models.CharField(max_length=4)
    percentage_c_or_g = models.CharField(max_length=4)
    ratio = models.CharField(max_length=4)
    cpg_sequence_2kb = models.TextField(blank=True)
    taxid = 9606
    classification = 'AM' 

    def __unicode__(self):
        return self.symbol

    class Meta:
       verbose_name = "human brain methylation change"


class K56Ac(models.Model):
    ensembl_gene = models.CharField(max_length=9, primary_key = True)
    level = models.FloatField()
    expression = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    pmid = 15882620 

    def __unicode__(self):
        return self.entrez_gene_symbol

    class Meta:
        verbose_name = "K56Ac"
        verbose_name_plural = "K56Ac"


class Pokholok(models.Model):
    ensembl_gene = models.CharField(max_length=19)
    chr = models.IntegerField()
    pos = models.IntegerField()
    h3_ypd = models.FloatField(blank=True)
    h4_ypd = models.FloatField(blank=True)
    h3_h2o2 = models.FloatField(blank=True)
    h3k9acvsh3_ypd = models.FloatField(blank=True)
    h3k14acvsh3_ypd = models.FloatField(blank=True)
    h3k14acvswce_ypd = models.FloatField(blank=True)
    h3k14acvsh3_h2o2 = models.FloatField(blank=True)
    h4acvsh3_ypd = models.FloatField(blank=True)
    h4acvsh3_h2o2 = models.FloatField(blank=True)
    h3k4me1vsh3_ypd = models.FloatField(blank=True)
    h3k4me2vsh3_ypd = models.FloatField(blank=True)
    h3k4me3vsh3_ypd = models.FloatField(blank=True)
    h3k36me3vsh3_ypd = models.FloatField(blank=True)
    h3k79me3vsh3_ypd = models.FloatField(blank=True)
    esa1_ypd = models.FloatField(blank=True)
    gcn5_ypd = models.FloatField(blank=True)
    gcn4_aa = models.FloatField(blank=True)
    gg_ypd = models.FloatField(blank=True)
    noab_ypd = models.FloatField(blank=True)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    pmid = 16122420

    def __unicode__(self):
        return self.ensembl_gene_id

    class Meta:
        verbose_name = "Histone modification"


class Acetylation(models.Model):
    ensembl_gene = models.CharField(max_length=9, primary_key=True)
    h4k8 = models.FloatField()
    h4k12 = models.FloatField()
    h4k16 = models.FloatField()
    h3k9 = models.FloatField()
    h3k14 = models.FloatField()
    h3k18 = models.FloatField()
    h3k23 = models.FloatField()
    h3k27 = models.FloatField()
    h2ak7 = models.FloatField()
    h2bk11 = models.FloatField()
    h2bk16 = models.FloatField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 4932
    pmid = 15186774

    def __unicode__(self):
       return self.ensembl_gene


class OneyrCbSpecific(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'cerebrellum'
    age = '1 year'

    def __unicode__(self):
        return self.gene

    class Meta:
       verbose_name = "one year cerebellum specific"
       verbose_name_plural = "one year cerebellum specific"


class OneyrHippSpecific(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=14)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'hippocampus'
    age = '1 year'

    def __unicode__(self):
        return self.gene

    class Meta:
       verbose_name = "one year hippocampus specific"
       verbose_name_plural = "one year hippocampus specific"

    
class AdultCbDynamic(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=14)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'cerebrellum'
    age = '6 weeks'

    def __unicode__(self):
        return self.gene

    class Meta:
       verbose_name = "adult cerebellum dynamic"
       verbose_name_plural = "adult cerebellum dynamic"
    

class AdultCbStable(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'cerebrellum'
    age = '6 weeks'

    def __unicode__(self):
        return self.gene

    class Meta:
        verbose_name = "adult cerebellum stable"
        verbose_name_plural = "adult cerebellum stable"

    
class AdultHippDynamic(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=14)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'hippocampus'
    age = '6 weeks'
    
class AdultHippStable(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'hippocampus'
    age = '6 weeks'

    def __unicode__(self):
       return self.gene

    class Meta:
       verbose_name = "adult hippocampus stable"
       verbose_name_plural = "adult hippocampus stable"


class CbSpecific(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'cerebrellum'

    def __unicode__(self):
        return self.gene

    class Meta:
         verbose_name = "cerebellum specific"
         verbose_name_plural = "cerebellum specific"

    
class HippSpecific(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'hippocampus'

    def __unicode__(self):
        return self.gene

    class Meta:
        verbose_name = "hippocampus specific"
        verbose_name_plural = "hippocampus specific"


class P7CbDynamic(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=15)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'cerebrellum'
    age = 'P7'

    def __unicode__(self):
        return self.gene

    class Meta:
        verbose_name = "P7 cerebellum dynamic"
        verbose_name_plural = "P7 cerebellum dynamic"

    
class P7HippDynamic(models.Model):
    chr = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    peak = models.CharField(max_length=14)
    p_value = models.FloatField()
    seq = models.TextField()
    gene = models.IntegerField()
    taxid = 9606
    tissue = 'hippocampus'
    age = 'P7'

    def __unicode__(self):
        return self.gene

    class Meta:
        verbose_name = "P7 hippocampus dynamic" 
        verbose_name_plural = "P7 hippocampus dynamic"


class Ultradian(models.Model):
    orf = models.CharField(max_length=7)
    gene = models.CharField(max_length=5)
    description = models.CharField(max_length=243)
    process = models.CharField(max_length=225,blank=True)
    component = models.CharField(max_length=65,blank=True)
    function = models.CharField(max_length=165,blank=True)
    f = models.IntegerField()
    o = models.FloatField(blank=True)

    def __unicode__(self):
        return self.gene

    class Meta:
        verbose_name = "Ultradian gene"


class Adult_Height_Association(models.Model):
    locus_rank = models.IntegerField()
    chr = models.CharField(max_length=5)
    gene_symbol = models.CharField(max_length=8)
    snp = models.CharField(max_length=10)
    effect_allele = models.CharField(max_length=1)
    male_effect = models.CharField(max_length=1)
    male_p = models.FloatField()
    female_effect = models.CharField(max_length=1)
    female_p = models.FloatField()
    phet_m_vs_f = models.FloatField()
    taxid = 9606
    classification = 'JA'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = "adult height association"


class BMAL1_Sites_Liver(models.Model):
    chromosome = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    distance = models.IntegerField()
    gene_symbol = models.CharField(max_length=18)
    biotype = models.CharField(max_length=23)
    mrna_pvalue = models.FloatField()
    mrna_phase = models.FloatField()
    e1 = models.IntegerField()
    e1_e2 = models.IntegerField()
    conservation = models.FloatField()
    zt2 = models.IntegerField()
    zt6 = models.IntegerField()
    zt10 = models.IntegerField()
    zt14 = models.IntegerField()
    zt18 = models.IntegerField()
    zt22 = models.IntegerField()
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    mapping = models.IntegerField(null=True, blank=True)
    taxid = 10090
    tissue = 'liver'

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
        verbose_name = "BMAL1 site liver"
        verbose_name_plural = "BMAL1 sites liver"


class DAM_Fernandez2011(models.Model):
    cpg_site = models.CharField(max_length=19)
    cgi = models.CharField(max_length=1)
    gene_symbol = models.CharField(max_length=11)
    correlation = models.FloatField()
    p_value = models.FloatField()

    def __unicode_(self):
       return self.gene_symbol

    class Meta:
        verbose_name = "aging differential methylated gene"
 

class DR_Essential(models.Model):
    taxid = models.IntegerField()
    classification = models.CharField(max_length=10)
    entrez_gene_id = models.IntegerField(null=True, blank=True)
    gene_symbol = models.CharField(max_length=30)

    def __unicode__(self):
        return self.gene_symbol

    class Meta:
       verbose_name = "DR-essential gene"
