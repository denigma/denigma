"""A library suite for references including and bilbiography.

For use of Medline and PubMed see:
http://www.nlm.nih.gov/bsd/pmresources.html

Use on search string to search 4 website catalogs:
http://stackoverflow.com/questions/7577145/simple-web-crawler-question-use-one-search-string-to-search-4-website-catalogs

See also:
http://utilitymill.com/edit/get_Book_Data_by_ISBNs
"""
import os
import re
import sys
import cPickle as pickle
import shelve

from Bio import Entrez
from Bio import Medline
Entrez.email = "hevok@denigma.de"

try:
    import denigma.apps.articles.google as google
except Exception as e:
    print e

try:
    from apps.articles.amazon import Search
except ImportError:
    print("Could not import Amazon search.")

if sys.platform == "linux2":
    PATH = '.'
else:
   PATH = 'D:/denigma/'


def q(s):
    """Performs a query."""
    terms = s.split()
    counts = None
    while not counts:
        #print terms
        records = Entrez.read(Entrez.esearch(db='pubmed', term=' '.join(terms)))
        counts = int(records['Count'])
        if not counts:
            terms = terms[1:]
        else: return records


def predefined(bib):
    bib.memo["Thaden JJ, Shmookler Reis RJ (2000) Ammonia, respiration, and longevity in nematodes. Age 23: 75-84."] = Reference(authors=['Thaden JJ', 'Shmookler Reis RJ'], 
    year=2000, 
    title="Ammonia, respiration, and longevity in nematodes: insights on metabolic regulation of life span from temporal rescaling", 
    journal="Age", volume=23, pages="75-84")

    bib.memo['Mussel C., Lausser L., Maucher M., Kestler H. A. (2012) Multi-Objective parameter selection for classifiers. Journal of Statistical Software 46:1-27'] = Reference(authors=["Mussel, C.", "Lausser, L.", "Maucher, M.", "Kestler, H. A."], year=2012, title="Multi-Objective parameter selection for classifiers.", journal="Journal of Statistical Software", volume="46", pages="1-27")
    bib.memo['Delongchamp RR, Lee TW, Shmookler Reis RJ (2011) Use of p-value plots to diagnose and remedy problems with statistical tests in microarray data. BMC Bioinformatics Epub ahead of print.'] = Reference(authors=["Delongchamp RR", "Lee TW", "Shmookler Reis RJ"], year=2011, title="Use of p-value plots to diagnose and remedy problems with statistical tests in microarray data.", journal="BMC Bioinformatics", volume="Epub ahead of print") 

    bib.memo['Delongchamp RR, Lee TW, Shmookler Reis RJ (2011) Use of p-value plots to diagnose and remedy problems with statistical tests in microarray data. BMC Bioinformatics Epub ahead of print.'] = Reference(authors=["Delongchamp RR", "Lee TW", "Shmookler Reis RJ"], year=2011, title="Use of p-value plots to diagnose and remedy problems with statistical tests in microarray data.", journal="BMC Bioinformatics", volume="Epub ahead of print")

    bib.memo['MARQ: an online tool to mine GEO for experiments with similar or opposite gene expression signatures. Nucleic Acids Res 38: W228-W232.'] = Reference(authors="Vazquez M, Nogales-Cadenas R, Arroyo J, Botias P, Garcia Carazo JM, Tirado F, Pascual-Montano A, Carmona-Saez".split(', '), title="MARQ: an online tool to mine GEO for experiments with similar or opposite gene expression signatures.", journal="Nucleic Acids Res", volume="38", pages="W228-W232")



class Bibliography(dict):
    def __init__(self, path=PATH):
        self.path = path
        if os.path.exists(os.path.join(PATH, 'bib.pkl')):
            print "Bibliography exists."
        try:
            data = pickle.load(open(os.path.join(self.path, 'bib.pkl'), 'rb'))
            self.update(data)
        except:
            "Did not load Bibliography."

       # self.memo = shelve.open(os.path.join(self.path, 'memo'))
            
        self.findings = [] # Stores the last fetched ids.
	
	#predefined(self)
            
    def save(self):
        pickle.dump(self, open(os.path.join(self.path, 'bib.pkl'), 'wb'))

    def exit(self):
        self.save()
        sys.exit()

    def find(self, query, printing=True):
        self.findings = []
        
        if str(query) in self.memo:
            return [self.memo[str(query)]]
        
        if isinstance(query, int):
            if query in self:
                result = [self[query]]
            else:
                result = self.fetch(query, printing=printing)
        else:
            result = self.decode(query, printing=printing)

        # Dynammic programming:
        if len(result) == 1:
            self.memo[str(query)] = result[0]
        else:
            # Take the top google hit:
            googled = False
            for url in google.search(query, stop=20):
                if url.startswith('http://www.ncbi.nlm.nih.gov/pubmed/'):
                    result = [self.efetch(int(url.split('/')[-1]), printing=printing)]
                    self.memo[str(query)] = result[0]
                    googled =  True
                    break

            # Amazone book query:
            if not googled:
##                title = query.split(')')[1].split('.')[0]
##                result = self.amazone(title)
##                print result
                try:
                    #data = Search(title=query.split(')')[1].split('.')[0]).result
                    data = Search(keywords=query).result
                    result = [Reference(**data)] ##authors=data['authors'], year=data['year'], title=data['title'], publisher=data['publisher'], date=data['date'], link=data['links'][0])]
                    self.memo[str(query)] = result[0]
                    print "Saved book as", str(query), result[0]
                except Exception as e:
                    print e

        return result


    def look(self, query):
        terms = query.replace(" et al., ", '').replace(" et al. ", '').split(' ')
        for pmid, reference in self.items():
            representation = str(reference)
            for term in terms:
                if term in representation:
                    pass
                else:
                    continue
                print representation
                return reference

    def efetch(self, id, printing=True, brief=False):
        """Fetches medline articles by pubmed ids:
        http://www.nlm.nih.gov/bsd/mms/medlineelements.html"""
        id = int(id)
        handle = Entrez.efetch(db="pubmed",id=id,rettype="medline",retmode="text")
        records = Medline.parse(handle)
        #print type(res)
        for r in records:
            if printing:
                for k,v in r.items():
                    pass
                    #print k, v
        try:
           reference = Reference(pmid=id,
                              title=r['TI'],
                              journal=r['TA'], # jounral abbreviation
                              alternate_journal=r['JT'], #journal title
                              abstract=r.get('AB', ''),
                              language=r['LA'][0],
                              authors=r.get('FAU', ''),
                              au=r['AU'],
                              date=r.get('EDAT', None),
                              issue=r.get('IP', ''),
                              volume=r.get('VI', ''),
                              pages=r.get('PG', ''),
                              keywords=r.get('MH', '')) # MeSH terms
           if reference.date:
              reference.year = reference.date.split('/')[0]
           else:
              reference.date = r['PHST']
              reference.year = reference.date[:4]

           if not reference.authors:
              try: 
                  reference.setAuthors(r['AU'])
              except Exception as e:
                  print e, r
                  try: 
                     reference.setAuthors(r['ROF'])
                  except Exception as e:
                     print e, r

           if printing:
              if not brief: print reference, '\n'
              else: print("{0} ({1}, {2}) {3}".format(reference.title, reference.etal, reference.year, reference.journal))
           return reference 
           
        except Exception as e:
            print "pmid = ", id
            print "Error = ", e
            print "Info = ", r
        #print reference
            


    def isdigit(self, id):
        try:
            int(id)
            return True
        except:
            return False
    
    def fetch(self, id, printing=False):
        if self.isdigit(id):
            references = [self.efetch(id, printing)]
        else:
            references = [] 
            #records = Entrez.read(Entrez.esearch(db='pubmed', term=id))
            records = q(id)
            for record in records['IdList']:
                result = self.efetch(record, printing)
                if result:
                    references.append(result)
                #references.append(efetch(record))
            #reference = references
        for reference in references:
            if reference.pmid not in self:
                self.findings.append(reference.pmid)
            self[reference.pmid] = reference
            
        return references#"Reference object with inital data"

    def undo(self):
        """Removes the last added references."""
        for i in self.findings:
            del self[i]

    def check(self, id, printing=False, brief=True):
        """Prints the title of a pmid."""
        return self.efetch(id, printing, brief)
            
    def summary(self, id, printing=False):
        handle = Entrez.esummary(db='pubmed', id=id)
        r = Entrez.read(handle)
        #print r[0]
        if printing:
            for k, v in r[0].items():
                print k,':', v
        r = r[0]
        ref = Reference(pmid=id, title=r['Title'], issue=r['Issue'], volume=r['Volume'], pages=r['Pages'], authors=r['AuthorList'], epub_date=r['EPubDate'], journal=r['FullJournalName'], year=r['PubDate'].split(' ')[0], language=r['LangList'][0] )
        if 'DOI' in r:
            ref.doi = r['DOI']
        return ref
    
    def add(self, id):
        summary_reference = self.summary(id=id)
        fetch_reference = self.fetch(id=id)
        reference = summary_reference + fetch_reference
        self[id] = reference

    def __len__(self):
        length = 0
        for i in self:
            length += 1
        return length

    def __repr__(self):
        L = []
        for k,v in self.items():
            L.append(repr(v))
        return "\n".join(L)

    def search(self, term, id=None, db='pubmed', add=False):
        if not id:
            handle = Entrez.esearch(db=db, term=term)
            record = Entrez.read(handle)
            print "Found %s publications" % record['Count']
            if add:
                for id in record['IdList']:
                    self.add(int(id))
            return record['IdList']
##        else:
##            Entrez.read(Entrz.esummary(db='pubmed', id=id)
##            return
    
    def decode(self, string, printing=False):
        """Takes a string of reference information and creates a
        reference object filled in with this information."""
        def isdigit(string):
            try:
                int(string)
                return True
            except:
                return False
        string = string.replace('\n', ' ')
        terms = re.findall('([\w,-]{2,})', string)
        print "terms:", terms
        #words = [i for i in terms if not isdigit(i) and i not in ['et', 'al', 'Suppl', 'Chem', 'Biol', 'RJ', 'MJ']]

        words = []
        for i in terms:
            if not isdigit(i) and i not in ['et', 'al', 'Suppl', 'Chem', 'Biol', 'RJ', 'MJ', 'Exp', '&', 'Sci', 'Med', 'Mol', 'Gerontol', 'BMC', 'Dev', 'Biochem', 'Epub', 'ahead', 'print', 'Biosyst', 'Nucleic', 'Acids', 'Res', 'W228-W232', 'Curr', 'S20', 'Proc', 'Natl', 'Acad', 'Mech', 'Rev', 'TW', 'Delongchamp',  'Cruz', 'V', 'Bioinformatics', 'Genes', 'Dev', 'Syst', 'Vis', 'May', 'pii', 'doi'] and i not in words and (":" not in i): # and "-" not in i
                print i
                words.append(i)
                
        print "words:", words
        year = re.findall('\(([0-9]{4})\)', string)
        if not year: year = re.findall('\(([0-9]{4})\)', string)
        print ' '.join(words+year)
        ref = bib.fetch(' '.join(words+year), printing)
        for i in ref:
            self[i.pmid] = i
        return ref #year, words#, ref

    def amazone(self, query):
        print query
        from amazone import API
        from key import AWS_KEY, SECRET_KEY
        ASSOC_TAG = 'Hevok'
        api = API(AWS_KEY, SECRET_KEY, 'us', ASSOC_TAG)
        node = api.item_search('Books', Title=query)
        results = []
        for page in node:
            for book in page.Items.Item:
                #print '%s' % (book.ASIN)
                #print dir(book)
                results.append(book.ASIN)
        return results

                  
class Reference():
    """s.k.a. class Publication()"""
    keys = {'journal':['fulljournalname'],
               'authors':['authorlist']}
    mapping = {}
    for k, v in keys.items():
        for i in v:
            mapping[i] = k
    def __init__(self, pmid=None, title=None, authors=None, year=None, abstract=None, keywords=None, link=None, url=None, journal=None, volume=None, issue=None, pages=None,
                 start_page=None, epup_date=None, date=None, type_of_article=None, short_title=None, alternate_journal=None, issn=None, doi=None, orignal_publication=None,
                 reprint_edition=None, reviewed_item=None, legal_note=None, pmcid=None, nihmsid=None, article_number=None, call_number=None, label=None, notes=None,
                 research_notes=None, file_attachment=None, author_address=None, figure=None, caption=None, access_date=None, translated_author=None, name_of_database=None,
                 database_provider=None, language=None, epub_date=None, orginal_publication=None, hihmsid=None, accession_number=None,
                 publisher=None, edition=None, isbn=None, city=None, au=None):

        if pmid: self.pmid = int(pmid)
        else: self.pmid = pmid
        self.title = title          
        self.authors = authors or []
        if authors:
            self.author = authors[0]
        self.au = au or self.authors # authors short names.
        self.abstract = abstract
        if keywords: self.keywords = keywords
        else: self.keywords = []
        self.link = link
        self.url = url
        self.journal = journal
        if year: self.year = int(year)
        else: self.year = year
        try: self.volume = int(volume)
        except: self.volume = volume
        if issue:
            try: self.issue = int(issue)
            except: self.issue = issue # Sometimes it is not an int, e.g. in '1-2' in Miller et al., 2005.
        else: self.issue = issue
        try: self.pages = int(pages)
        except: self.pages = pages
        if start_page: self.start_page = int(start_page)
        else: self.start_page = start_page
        self.epub_date = epub_date
        self.date = date
        self.type_of_article = type_of_article
        self.short_title = short_title
        self.alternate_journal = alternate_journal
        self.issn = issn
        self.doi = doi
        self.orginal_publication = orginal_publication
        self.reprint_edition = reprint_edition
        self.reviewed_item = reviewed_item
        self.legal_note = legal_note
        self.pmcid = pmcid
        self.nihmsid = hihmsid
        self.article_number = article_number
        self.accession_number = accession_number
        self.call_number = call_number
        self.label = label
        self.notes = notes
        self.research_notes = research_notes
        self.file_attachment = file_attachment
        self.author_address = author_address
        self.figure = figure
        self.caption = caption
        self.access_date = access_date
        self.translated_author = translated_author
        self.name_of_database = name_of_database
        self.database_provider = database_provider
        self.language = language
        self.city = city or ''

        # Books attributes:
        self.publisher = publisher
        self.edition = edition
        self.isbn = isbn
        

    def __add__(self, other):
        for k,v in vars(other).items():
            attribute = eval('self.'+k)
            if v:
                if not attribute:
                    if isinstance(v, int) or isinstance(v, list):
                        exec('self.'+k+'='+v)
                    elif isinstance(v, str):
                        if k == 'abstract': exec('self.'+k+'="""'+v+'"""')
                        else: exec('self.'+k+'="'+v+'"')
                elif attribute and attribute != v: print "Mismatch:", k, attribute, v
        return self

    def aus(self):
       """Inferes the short names from the full names."""
       for author in self.authors:
           naming = []
           names = split(' ')
           lastname = names[0]
           naming.extend([lastname, ' '])
           for name in names[1:]:
              naming.append('')

    def ref(self):
        #self.year = self.epub_date.split(' ')[0]
        if len(self.authors) == 1:
            return "%s, %s" % (self.authors[0].split(', ')[0], self.year)
        elif len(self.authors) == 2:
            return "%s & %s, %s" % (self.authors[0].split(', ')[0], self.authors[1].split(', ')[0], self.year)
        else:
            try: return "%s et al. %s" % (self.authors[0].split(', ')[0], self.year)
            except: return "No Author et al. 2013"
    def __repr__(self):
        return "%s %s %s" % (self.pmid, self.ref(), self.title)

    def full(self):
        if  hasattr(self, 'publisher') and  self.publisher: # Book! 
         #print self.title
            # http://www.ltu.edu/cm/attach/48B22909-07C8-4001-BF4F-8F5608BE7A27/How%20to%20Cite%20Sources%20in%20an%20Academic%20Paper.pdf
            # [name].[year of publication].[title, italiced].[city:name of publisher]. 
            return "%s (%s) *%s*.%s: %s" % (", ".join(self.au), self.year, self.title, self.city, self.publisher) #self.edition#, self.pages)
        else: # No book. Need to check, because old bibliography records have publisher attribute.
            if self.volume and self.pages:
                return "%s (%s) *%s* %s %s: %s." % (", ".join(self.au), self.year, self.title, self.journal, self.volume, self.pages)
            else: 
                return "%s (%s) *%s* %s." % (", ".join(self.au), self.year, self.title, self.journal)

   

    def __str__(self):
        L = []
        for k,v in vars(self).items():
            if v: L.append("%s = %s" % (k, v))
        return "\n".join(L)

    def related(self, top=5):
        """Retrieves related references, but does not add them."""
        self.relations = []
        record = Entrez.read(Entrez.elink(dbfrom="pubmed", id=self.pmid))
        #print record
        for pmid in record[0]["LinkSetDb"][0]["Link"][:top]:
            self.relations.append(bib.check(pmid["Id"]))
            #print pmid
        #return self.relations
            
    def cited(self, top=5):
        """Retrieves publiction which cite this reference."""
        self.citations = []
        pmcids = Entrez.read(Entrez.elink(dbfrom="pubmed", db="pmc",
                                           LinkName="pubmed_pmc_refs",
                                           from_uid=self.pmid))
        pmcids = [i.values()[0] for i in pmcids[0]['LinkSetDb'][0]['Link'][:top]] #.values() #[:5]
        pmids = Entrez.read(Entrez.elink(dbfrom="pmc", db="pubmed",
                                         LinkName="pmc_pubmed",
                                         from_uid=",".join(pmcids)))
        for pmid in [i.values()[0] for i in pmids[0]['LinkSetDb'][0]['Link']]:
            self.citations.append(bib.check(pmid))
        #return self.citations

    def etal(self):
        """Returns last name of first author, et al."""
        return self.author.split(', ')[0]+' et al.'
    etal = property(etal)

    def setAuthors(self, authors):
        """Sets the list of authors as well as the primary author."""
        if isinstance(authors, list): pass
        elif isinstance(authors, str):
            if '; ' in authors:
                authors = authors.split('; ')
        self.authors = authors
        self.author = authors[0]

    def decipher(self, query):
        query = query.split('.')
        print query
       
bib = Bibliography()

    
if __name__ == '__main__':
    #res = bib.search(22457769)
    #bib.summary(22457769)
    #bib.add(22457769)
    #ref = bib.fetch(10708258)
    #print ref.related()
    #ref = bib.fetch("Regulation of lifespan by sensory perception in Caenorhabditis elegans")
    #refs = bib.decode("Coburn, C. M., Mori, I., Ohshima, Y., and Bargmann, C. I. (1998). A cyclic nucleotide-gated channel inhibits sensory axon outgrowth in larval and adult Caenorhabditis elegans: a distinct pathway for maintenance of sensory axon structure. Development 125",
    #                  printing = True)
    #print bib.decode("Komatsu, H., Mori, I., Rhee, J. S., Akaike, N., and Ohshima, Y. (1996). Mutations in a cyclic nucleotide-gated channel lead to abnormal thermosensation and chemosensation in C. elegans. Neuron 17, 707-18.")
    #print bib.decode("Rudolph, K. L., Chang, S., Lee, H. W., Blasco, M., Gottlieb, G. J., Greider, C., and DePinho, R. A. (1999). Longevity, stress response, and cancer in aging telomerase-deficient mice. Cell 96, 701-12")

##    from mapping import m
##    from omics import genes, Genes, Proteins
    #genes.load()
    #uniprot = Genes("UniProt")
    #print bib.decode("Dillin, A. et al. Science 298, 2398-2401 (2002)")
    #print bib.decode("Nunez Heard Narita Lin Hearn Spector Hannon Lowe Rb mediated heterochromatin formation and silencing of E2f target genes during cellular senescence Cell 2003")
    #bib.find(16103914)
    #bib[18516045].related()
    #bib[18516045].cited()
    #bib.decipher("""Wolfe RR, Chinkes DL (2005) Isotope Tracers in Metabolic Research: Principles and Practice of Kinetic Analysis. Hoboken NJ: Wiley.""")
    #r = bib.find("Wolfe RR, Chinkes DL (2005) Isotope Tracers in Metabolic Research: Principles and Practice of Kinetic Analysis. Hoboken NJ: Wiley.")
    r = bib.find("Kenyon C, Chang J, Gensch E, Rudner A, Tabtiang R (1993) A C. elegans mutant that lives twice as long as wild type. Nature 366: 461-464.")
    ref = Reference(title='Dissecting the Gene Network of Dietary Restriction to Identify Evolutionarily Conserved Pathways and New Functional Genes',
                    authors=['Wuttke, Daniel', 'Connor, Richard', 'Vora, Chintan', 'Craig Thomas', 'Li, Yang', 'Wood, Shona',
                             'Vasieva, Olga', 'Shmookler, Reis', 'Tang, Fusheng', 'de Magalhaes, Joao Pedro'],
                    abstract="""Dietary restriction (DR), limiting nutrient intake from diet without causing malnutrition, delays the aging process and extends lifespan in multiple organisms. The conserved life-extending effect of DR suggests the involvement of fundamental mechanisms, although these remain a subject of debate. To help decipher the life-extending mechanisms of DR, we first compiled a list of genes that if genetically altered disrupt or prevent the life-extending effects of DR. We called these DR essential genes and identified over 100 in model organisms such as yeast, worms, flies and mice. In order for other researchers to benefit from this first curated list of genes essential for DR, we established an online database called GenDR (http://genomics.senescence.info/diet/). To dissect the interactions of DR-essential genes and discover the underlying lifespan-extending mechanisms, we then used a variety of network and systems biology approaches to analyze the gene network of DR. We show that DR-essential genes are more conserved at the molecular level and have more molecular interactions than expected by chance. Furthermore, we employed a guilt-by-association method to predict novel DR-essential genes. In budding yeast, we predicted nine genes related to vacuolar functions; we show experimentally that mutations deleting eight of those genes prevent the life-extending effects of DR. Three of these mutants (OPT2, FRE6 and RCR2) had extended lifespan even under ad libitum, indicating that the lack of further longevity under DR is not caused by a general compromise of fitness. These results demonstrate how network analyses of DR using GenDR can be used to make phenotypically-relevant predictions. Moreover, gene-regulatory circuits reveal that the DR-induced transcriptional signature in yeast involves nutrient-sensing, stress-responses and meiotic transcription factors. Finally, comparing the influence of gene expression changes during DR on the interactomes of multiple organisms led us to suggest that DR commonly suppresses translation, while stimulating an ancient reproduction-related process.""",
                    keywords=['Aging', 'Diet', 'Evolution', 'Interactome', 'Systems biology'],
                    journal='PLoS Genetics', year=2012)
    bib['Dissecting the Gene Network of Dietary Restriction to Identify Evolutionarily Conserved Pathways and New Functional Genes'] = ref
    bib.memo['Wuttke et al. 2012'] = ref
                    
