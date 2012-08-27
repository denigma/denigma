# -*- coding: utf-8 -*-
import datetime

from datasets.models import Reference, GenAge, Intervention, Change
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q


def update(request):
    from Bio import Entrez
    from Bio import Medline
    Entrez.email = "hevok@denigma.de"
    
    print "updating"
    references = Reference.objects.all()
    for i in references:
        try:
            handle = Entrez.esummary(db='pubmed', id=i.pmid)
            r = Entrez.read(handle)
            #or k, v in r[0].items():
                    #print k,':', v
            #print type(r)

            r = r[0]
            i.title=r['Title']
            #print i.pmid, type(i.pmid), i.title
            i.issue=r['Issue']
            #print i.issue
            i.volume=r['Volume']
            #print i.volume
            i.pages=r['Pages']
            #print i.pages
            i.authors='; '.join(r['AuthorList'])
            #print "authorslenght", len('; '.join(r['AuthorList']))
            #print i.authors
            #i.epub_date=datetime.date(r['EPubDate'])
            #print i.epub_date
            i.journal=r['FullJournalName']
            i.year=int(r['PubDate'].split(' ')[0])
            #print i.year
            i.language=r['LangList'][0]
            #print i.language

##            handle = Entrez.efetch(db="pubmed",id=id,rettype="medline",retmode="text")
##            records = Medline.parse(handle)
##            for r in records: pass
##            i.abstract=r['AB']
            
            i.save()
        except ValueError:
            print "Error, by retrieving pubmed data.", i.pmid, len(r), type(r)
            try:
                for k, v in r[0].items():
                    print k,':', v
            except KeyError: "Print got an KeyError"
        except: print('Failed retieving information for %s' % i)
    return HttpResponse('Updated!')


def describe(request):
    """Annotates the AgeFactor table with description from various sources.
    Put everything into a seperate thread."""
    from Annotations import Annotation

    print("Restrict to genes for now:")
    factors = GenAge.objects.filter(entrez_gene_id__isnull=False)
    all = GenAge.objects.all()
    print len(factors), len(all)

    # Get a dict of all entrez ids:
    ids = [factor.entrez_gene_id for factor in factors]
    # Pass it to Annotation:
    genes = Annotation.describe(ids)

    for factor in factors:
        if factor.entrez_gene_id in genes:
            #try:
            factor.description = genes[factor.entrez_gene_id].description or ''
            #factor.description.replace(r"\xCE\xB1", 'alpha').replace(r"0xce", '')
            #factor.description.encode('utf-8')
            #except:
                #pass
            #
        #print factor.description
            factor.save()
        else: print factor.entrez_gene_id, factor.symbol, factor.name
    print "Done"
    
    return HttpResponse('Description function works!')

def isdigit(num):
    try: return int(num)
    except: return False

def functional_description(request):
    """Unites the function and description fields."""   
    import re
    p = '\D\D\D; \D\D\D' # non pmid boundaries
    def repl(string):
        string = string.group(0)
        string = string.replace('; ', '##')
        return string
    
    count = 0
    genes = GenAge.objects.all()
    for gene in genes:

        
        functions = re.sub(p, repl, gene.function)
        functions = functions.split('##')

        #description = gene.description
        
        descriptions = gene.description.split('; ')
        described = False
        for descr in descriptions:
            if descr.endswith('[UniProt]'):
                description = descr
                described = True
                break
        if not described:
            description = '; '.join(descriptions)
        descriptions = set(description.split(' '))
            
        for function in functions:
            if isdigit(function[:-3]) or isdigit(function[:3]): continue # ignore pmids
            terms = set(function.split(' '))
            intersection = terms.intersection(descriptions)
            if intersection and len(intersection) < len(terms)*0.4:
                gene.functional_description = function+'; '+description
                count += 1
            else:
                if gene.description:
                    gene.functional_description = description
                else:
                    gene.functional_description = gene.function
        gene.save()
    return HttpResponse('%s functions and discription united.' % count)

def integrity(request):
    """Checks for the quility of database records.
    e.g. are all annotations up to date, no naming conflicts.
    no duplicates, etc."""
    from mapping import m

    factors = GenAge.objects.exclude(intervention__manipulation__shortcut='DT') #(filter(~Q)
    taxids = []
    ids = []
    dups = duplicates("GenAge")
    noclasses = []
    nointervention = []

    for factor in factors:

        # Missing Taxonomy identifier:
        if not factor.taxid:
            taxids.append(factor)

        # Missing primary id:
        if not factor.entrez_gene_id and factor.symbol not in ['CKIepsilon', 'cyc1', 'Y46G5A.6']:


            #missed = '\t'.join(map(str, [factor.entrez_gene_id, factor.symbol,

            #if factor.symbol:print m(factor.symbol, factor.taxid)
            #print missed
            #print type(m), type(factor.symbol), type(factor.taxid)
            synonyms =[]
            factor.alias = set()
            if factor.symbol:
                synonyms.append(str(factor.symbol))
            if factor.name:
                synonyms.append(str(factor.name))
            try:
                mapped = m(synonyms, factor.taxid)
                factor.id = mapped[0]
                factor.ensembl = mapped[1]['ensembl_gene']
                for k,v in mapped[1].items():
                    if isinstance(v, list):
                        continue
                        for i in v:
                            factor.alias.add(i)
                    else:
                        factor.alias.add(v)
            except Exception as e:
                print e, factor
            factor.alias = '; '.join(list(map(str, factor.alias)))

            #factor.mapped = mapped

            ids.append(factor)

        # Are all genes classified?
        #print factor.classifications.all()
        try:
            if not factor.classifications.all():
                #print factor.symbol, "has no classification associated."
                noclasses.append(factor)
        except Exception as e:
            print e, factor.id, factor.symbol, "failed"

        # Links to interventions:
        try:
            if not factor.intervention.all():
                #print factor.symbol, "is not linked to an intervention"
                nointervention.append(factor)
        except Exception as e:
            print e, factor.id, factor.symbol, "failed"
    #print len(noclasses), "Unclassified."
    #print len(nointervention), "without an intervention associated."
    nc = set([factor.entrez_gene_id for factor in noclasses])
    ni = set([factor.entrez_gene_id for factor in nointervention])
    intersection = nc & ni
    print "Intersection: ", len(intersection)
            


        
    return render_to_response('genage_integrity.html', {'taxids':taxids,
                                                            'ids':ids,
                                                            'dups':dups,
                                                            'noclasses':noclasses}) #HttpResponse#'\n'.join(missing))

def duplicates(table):
    """Identifies duplicates entries in a tablevbased on unique identifiers
    (i.e. entrez gene IDs)."""
    ids = {}
    dups = []
    records = eval(table+'.objects.all()')
    for record in records:
        id = record.entrez_gene_id
        if id:
            if id in ids:
                dups.extend([record, ids[id]])
                print id
            else: ids[id] = record
    return dups



def replace(request, table, field, term, by):
    """Replaces a string in a filed by another string."""
    print request, field, term, by
    records = eval(table+'.objects.all()')
    pre = []
    post = []
    result  = ''
    for record in records:
        attr = getattr(record, field)
        if term in attr:
            print
            print record.id
            print attr
            print
            pre.append(attr)
            mod_attr = attr.replace(term, by)
            print mod_attr
            post.append(mod_attr)
            setattr(record, field, mod_attr)
            print #getattr(record, field)
            record.save()
    for index, string in enumerate(pre):
        result += '\n'.join([pre[index]+'\n'+post[index]])#
    return HttpResponse("Replace in table %s field %s the term %s by %s\n%s" % (table, field, term, by, result))

def dump(request):
    """Dumps information from GenAge out to a file (GenDR by default)."""
    import re
    from scripts.c import multiple_replace
    
    output = open("GenDR.txt", 'w')
    output.write("\t".join(["entrez_gene_id", "ensembl_gene_id", "taxid", "symbol", "name", "alias", "function", "description", "functional_description", "observation", "regimens", "lifespans", "references"])+'\n') #"classifications", 
    #genes = GenAge.objects.all()
    genes = GenAge.objects.filter(classifications__shortcut='DE')
    print len(genes)
    for gene in genes:
        #classifications = gene.classifications.all()
        #classes = []
        #for classification in classifications:
         #classes.append(classification.shortcut)
        regimens = gene.regimen.all()
        regimes = []
        for regimen in regimens:
         regimes.append(regimen.shortcut)
        aliases = gene.alias.replace(';', '; ')
        lifespan = gene.lifespan.all()
        lifespans = [ls.shortcut for ls in lifespan]
        if ("Geber et al., unpublished" not in gene.reference and "Tang et al., unpublished" not in gene.reference): #"DE" in classes and
          
            description = gene.description #decode('utf-8')
            description = description.replace(u'β','Beta')
            if description:
                description = description.encode('utf-8') #[0]
            functional_description = gene.functional_description
            functional_description = functional_description.replace(u'β','Beta')

            references = set()
            pattern = '\[(.+?)\]'
            findings = re.findall(pattern, str(gene.observation))
            for finding in findings:
                items = finding.replace('; ', ';').split(';')
                for item in items:
                    print item
                    references.add(item)
            
            try:
                output.write("\t".join(map(str, [gene.entrez_gene_id,
                                                     gene.ensembl_gene_id,
                                                     gene.taxid,
                                                     gene.symbol,
                                                     gene.name,
                                                     aliases,
                                                     gene.function,
                                                     description,
                                                     functional_description.encode('utf-8'),
                                                     multiple_replace(gene.observation, {'\n':' ','\r':' '}),
                                                     #"; ".join(classes),
                                                     "; ".join(regimes),
                                                     "; ".join(lifespans),
                                                     "; ".join(references)])) +'\n'    )         
            except:
                print "gene symbol:", gene.symbol
                print gene.description
                print gene.functional_description
                #
                print
    print "done"
    return HttpResponse("GenDR was succefully saved.")

##      elif  "DE" in classes:
##         print gene.symbol, gene.reference

#dump()
#stop

def show_all(request):
    references = Reference.objects.all()
    return render_to_response('references.html', {'references': references})
    
    
