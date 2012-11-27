"""Signature classes"""
import os
import shelve
#import marshal

from numpy import arange

from omics.gen import Genes, Gene, genes
from scripts.c import intersect
from stats.pValue import hyperg
try: from mapping import m
except: "Print failed to import mapping"

if os.name == 'posix':
    PATH = '/media/SDATA1'
elif os.name == 'nt':
    PATH = 'D:/Signatures/'


def up(name):
	print ' '.join(S[name].up)

	
def down(name):
	print ' '.join(S[name].up)

	
def s():
    for v in signatures.values():
        print v.name, v.tissue, v.expression(pvalue=0.05)
        

class Signatures(dict):
    """A collection of signatures."""
    def __init__(self, name=None, groups=None):
        dict.__init__(self)
        self.name = name
        if not groups: self.groups = []

    def add(self, *signatures):
        """Add one or more signatures to the signature collection.
        Signature to be added requrie a unique name."""
        for signature in signatures:
            self[signature.name] = signature

    def __repr__(self):
        string = '%s:\n' % (self.name)
        for signature in self:
            string += self[signature].__repr__()+'\n'
        return string

    def __str__(self):
        import shelve
        signatures = shelve.open("D://signatures/signatures")
        for signature in signatures.keys():
            print signature

    def expression(self, ratio=2.0, pvalue=None):
        """Triggers the calculation of differential expression for each signature."""
        for signature in self:
            self[signature].expression(ratio, pvalue)
        
    def gene(self, gene):
        """Retreives the information of a specific gene in all signatures."""
        for signature in self:
            print signature
            try: print self[signature][gene]
            except KeyError: print "Not found"
        
    def pValues(self):
        """Triggers the calculation of p-vales for each gene in each signature."""
        for signature in self:
            self[signature].pValues()

    def read(self, taxid=None, title=None, names=None):
        if names and type(names) == list:   # or type(names) == dict:
            for name in names: pass

    def compara(self, S1, S2):
        """Compares two signatures for significant overlap."""
        if isinstance(S1, str): S1 = self[S1] # if only the name is given
        if isinstance(S2, str): S2 = self[S2] # the signature will be identfied

        if len(S1) > len(S2): total = len(S1)
        else: total = len(S2)
        S1_ranked_list = []
        S2_ranked_list = []
        for gene in S1:
            S1_ranked_list.append((S1[gene].ratio, S1[gene]))
        S1_ranked_list.sort()
        #S1_ranked_list.reverse()
        for gene in S2:
            S2_ranked_list.append((S2[gene].ratio, S2[gene]))
        S2_ranked_list.sort()
        #S2_ranked_list.reverse()
        print len(S1_ranked_list), len(S2_ranked_list)
        for threshold in xrange(100,5000,100):
            S1.up = {}
            S2.up = {}
            for ratio, s1 in S1_ranked_list[:threshold]: S1.up[s1.id] = s1
            for ratio, s2 in S2_ranked_list[:threshold]: S2.up[s2.id] = s2
            Intersection = intersect(S1.up, S2.up)
            pvalue = hyperg(len(S1.up), len(S2.up), total, len(Intersection))
            print  threshold, '\t', len(S1.up), '\t', len(S2.up), '\t', len(Intersection), '\t', pvalue# len(IntersectionUp), pvalueUp, len(S1.down), len(S2.down), len(IntersectionDown), pvalueDown, len(IntersectionComb), pvalueComb

    def compare(self, S1, S2, lower=1, upper=99, step=0.1):
        """Compares two signatures for significant overlap."""
        if isinstance(S1, str): S1 = self[S1] # if only the name is given
        if isinstance(S2, str): S2 = self[S2] # the signature will be identfied
    ##    O = Organisms[S.taxid].number_genes
        #if S1.type != 'profile' and S2.type != profile:
        if len(S1) > len(S2): total = len(S1)
        else: total = len(S2)
        #total = 6600
        Range = arange(lower, upper, step).tolist()
        for upper in Range:
            lower = 1/upper

    ##        if S1.type == 'profile':
            S1.delta = {}
            S1.up = {}
            S1.down = {}        
            for s1 in S1:
                if S1[s1].ratio > upper or not S1[s1].ratio: #or S1[s1].ratio < lower:
                    S1.delta[s1] = S1[s1]
    ##                if S1.genes[s1].fold_change > upper:
    ##                    S1.up[s1] = S1.genes[s1]
    ##                else:
    ##                    S1.down[s1] = S1.genes[s1]

    ##        else:S1.delta = S1.genes

    ##        if S2.type == 'profile':        
            S2.delta = {}
            S2.up = {}
            S2.down = {}
            for s2 in S2:
                #print s2, type(s2), S2[s2].fold_change, hasattr(S2[s2], 'fold_change')
                if S2[s2].ratio > upper or not S2[s2].ratio:#S2[s2].ratio < lower:
                    S2.delta[s2] = S2[s2]
    ##                if S2.genes[s2].fold_change > upper:
    ##                    S2.up[s2] = S2.genes[s2]
    ##                else:
    ##                    S2.down[s2] = S2.genes[s2]

    ##        else: S2.delta = S2.genes
            #print len(S1.delta), len(S2.delta)
            Intersection = intersect(S1.delta, S2.delta)
            
    ##        IntersectionUp = intersect(S1.up, S2.up)
    ##        IntersectionDown = intersect(S1.down, S2.down)
    ##        IntersectionComb = union(IntersectionUp, IntersectionDown)
            if not len(S1.delta) or not len(S2.delta) or not Intersection: return None
            pvalue = hyperg(len(S1.delta), len(S2.delta), total, len(Intersection))

    ##        pvalueComb = hyperg(len(S1.delta), len(S2.delta), total, len(IntersectionComb))
    ##        pvalueUp = hyperg(len(S1.up), len(S2.up), total, len(IntersectionUp))
    ##        pvalueDown = hyperg(len(S1.down), len(S2.down), total, len(IntersectionDown))
            
            print  upper, '\t', len(S1.delta), '\t', len(S2.delta), '\t', len(Intersection), '\t', pvalue# len(IntersectionUp), pvalueUp, len(S1.down), len(S2.down), len(IntersectionDown), pvalueDown, len(IntersectionComb), pvalueComb
    ##        if pvalue < 0.05 and pvalue != 0:
    ##        if len(Intersection) == 4:
    ##            for i in Intersection: print S1.genes[i].symbol, S1.genes[i].fold_change
    ##            stop
    ##        print S1.genes[Result[0]].symbol, S2.genes[Result[0]].fold_change
        return len(S1.delta.keys()), len(S2.delta.keys()), len(Intersection)

    def enriched(self, S1, S2, ratio=1.0, upper=None, step=0.1, pvalue=None):
        """Compares two signatures for significant overlap."""
        if isinstance(S1, str): S1 = self[S1] # if only the name is given
        if isinstance(S2, str): S2 = self[S2] # the signature will be identfied
        if len(S1) > len(S2): total = len(S1)
        else: total = len(S2)

        if not upper: upper = 99
        Range = arange(ratio, upper, step).tolist()
        for upper in Range:
            lower = 1/upper
            S1.delta, S1.up, S1.down = {}, {}, {}
            S2.delta, S2.up, S2.down = {}, {}, {}
            for gene in S1:
                if S1[gene].ratio > upper: #or not S1[gene].ratio:
                    if pvalue:
                        if S1[gene].pvalue < pvalue: S1.up[gene] = S1[gene]
                    else: S1.up[gene] = S1[gene]
            for gene in S2:
                if S2[gene].ratio > upper or not S2[gene].ratio:
                    if pvalue:
                        if S2[gene].pvalue < pvalue: S2.up[gene] = S2[gene]
                    else: S2.up[gene] = S2[gene]
            Intersection = intersect(S1.up, S2.up)
            if not S1.up or not S2.up or not Intersection: break
            pvalue = hyperg(len(S1.up), len(S2.up), total, len(Intersection))
            print upper, len(S1.up), len(S2.up), len(Intersection), pvalue, ', '.join(Intersection)

    def search(self, name=None, path=PATH):
        """Searches s signatures matching a term.
        If succesfull it triggers generate function to derive a signature directly from file."""
        if name:
##            listdir = os.listdir(os.path.join(path))
##            for f in listdir:
##                if name in f:
##                    print f
##                    if os.path.isdir(os.path.join(path, f)): print os.listdir(path+'/'+f)
##                    print
##                    if 'factor=' in f and name in f: print f
##                    self.generate(path+'/'+f, name)
##                if os.path.isdir(os.path.join(path, f)):
##                    self.search(path=path+'/'+f,name=name)
            taxids = os.listdir(path)                  
            for taxid in taxids:
                try: taxid = int(taxid)
                except: pass
                if type(taxid) == int:
                    titles = os.listdir(os.path.join(path, str(taxid)))
                    for title in titles:
                        files = os.listdir(os.path.join(path, str(taxid), title))
                        for f in files:
                            if name in f and f.endswith('.txt'):
                                self.generate(path, taxid, title, f)
                

    def generate(self, path, taxid, title, f):
        
##        print f
##        Input = file(f).read().split('\n')
##        print len(Input)
##        for line in Input:
##            s = line.split('\t')
##            if line == Input[0]:
##                header = {}
##                for x in xrange(0, len(s)):
##                    header[x] = s[x]
##                    
##                if "name=" in signature:
##                    name = signature.split('name=')[1].split(';')[0]
##                print signature
##                taxid = signature.split('D:/Signatures/')[1].split('/')[0]
##                print name, taxid
##                signature = Signature(name=name, taxid=taxid)
##                continue
##            for x in xrange(0, len(s)):
##                gene = Gene(
##                signature[gene]
        #sig = 'A spatial and temporal map of C. elegans gene expression'
        #f = filepath.split(' C. elegans gene expression/')[1]
        #taxid = filepath.split('D:/Signatures//')[1].split('/')[0]
        #print taxid
        
        signature_info = f.replace('.txt', '').split(';')
        name = []

        for s in xrange(len(signature_info)):
            splited = signature_info[s].split('=')
            signature_info[s] = splited[0]+'="'+splited[1]+'"'
            print signature_info[s]
            if 'name=' not in f:
                name.append(splited[1])
        if 'name=' not in f:
            name = ' '.join(name)
            signature_info.extend(['title=title', 'name=name', 'taxid=int(taxid)']) 
        else: signature_info.extend(['title=title', 'taxid=int(taxid)'])

        print signature_info
        S = eval('Signature('+", ".join(signature_info)+')')
        if S.name not in self:
##                    Signatures.append(S)                   
            input = file(os.path.join(path, str(taxid), title, f)).read().split('\n') #filepath).read().split('\n') #
            
            info = {}       #Provides a mapping of the header to fascilate gene info matching.
            c = 0
            for column in input[0].split('\t'):
                info[c] = column.lower().replace(' ', '_')
                if info[c] in Gene.mapping: info[c] = Gene.mapping[info[c]]
                if info[c] not in Gene.keys: print '...', info[c]#, "Warning! Could not recoqnise: ", 
                c += 1
                
            L = len(input); n = 0; PB = 0 #Start Counter

            for i in input:

                n += 1; PA = 100*n/L #Continue Counter
                if PA != PB: print PA,
                PB = PA
                
                if i != input[0] and i != "":
                    #print len(i)
                    i = i.replace('"', '')  #Cleans up all the Excel inserted " strings marks.
                    #print i

                    columns = i.split('\t')
                    gene_info = []
                
                    c = 0

                    fold_change = []
                    ratio = []
                    
                    for column in columns:
                        if column != "" and column != '#N/A' and column != '#DIV/0!' and c in info:

                            #determine whether it is a an integer, float or string:
                            try:
                                if column == "nan" and info[c] == "gene_symbol": mapping = '"'+column+'"'
                                elif "." in column: mapping = str(float(column))
                                else: mapping = str(int(column))
                            except:
                                mapping = '"'+column+'"'
                                mapping = mapping.replace('\xa0','')

                            if info[c] in Gene.mapping:
                                info[c] = Gene.mapping[info[c]]
                            if info[c] in Gene.keys:
                                gene_info.append(info[c]+'='+mapping)
##                                    else: print "Couldn't recoqnise: ", info[c], S.name, S.title
                                #print gene_info

                            #If multiple fold_changes are giving average them
                            if "fold_change" in info[c] and info[c] != "fold_change" and mapping != "":
                                fold_change.append(float(mapping))

                            if "ratio" in info[c] and info[c] != "ratio" and mapping != "":
                                ratio.append(float(mapping))

                        c += 1
                        
                    if fold_change != [] and 'fold_change' not in "".join(gene_info):
                        fold_change = sum(fold_change)/len(fold_change)    
                        gene_info.append('fold_change='+mapping)
                        
                    if ratio != [] and 'ratio' not in "".join(gene_info):
                        ratio = sum(ratio)/len(ratio)    
                        gene_info.append('ratio='+mapping)
                        
                    if 'taxid' in ' '.join(info.values()):  #http://stackoverflow.com/questions/2536625/how-do-i-join-the-values-of-nested-python-dictionary
                        G = eval('Gene('+", ".join(gene_info)+')')
                    else:
                        G = eval('Gene('+", ".join(gene_info)+', taxid='+str(taxid)+')')
                        
                    G.alsoKnownAs()
                    if not G.id: G.id = m(map(str, G.aka), int(taxid))[0]  #Deactive if prociding should be without mapping
                    if G.ensembl_gene == '': G.ensembl_gene = m.it(map(str, G.aka), int(taxid))[1]
                    if G.ensembl_gene and G.ensembl_gene[0] not in S: S[G.ensembl_gene[0]] = G #print "Couldn't map ", G.alias
                    #if G.id and G.id not in S.genes: S.genes[G.id] = G
                    elif G.id and G.id in S: S[G.id].merge(G) # Does it actually work?
                    elif G.ensembl_gene and G.ensembl_gene in S: S[G.ensembl_gene[0]].merge(G)# #print "Couldn't map ", G.alias
                    elif G.ensembl_gene: S[G.ensembl_gene] = G #print "Couldn't map ", G.alias
                    #print len(S)
            self[S.name] = S                                

    def save(self, path=None, name=None):
        """Serializes the signatures."""
        for signature in self.values():
            if signature:
                signature.save(path, name)

        # Dumb meta data:
        
            
    def load(self, path=None):
        """Deserializes signatures."""
        if not path: path = 'D:/Signatures/'
        files = os.listdir(path)
        for f in self:
            if '.' not in f:
                signature = Signature()
                signature.load(os.path.join(path, f))
                self[signature.name] = signature

    def serialize(self, signature):
        """Stepwise serialziation of added signatures."""
        self.add(signatures)
        signature.save()
        self[signature].clear()

    def find(self, term):
        """Finds all signatures which contain the specified term."""
        import shelve
        signatures = shelve.open('D://signatures/signatures')
        for signatures in signatures.keys():
            if term in signatures:
                print signature
        signatures.close()

            
    def summary(self):
        """Prints out name, tissue, and how many genes were differentially expressed."""
        for v in signatures.values():
            print v.name, v.tissue, v.expression(pvalue=0.05)  
                    

class Signature(dict):
    '''A molecular signature is like a fingerprint, basicely its just a list of genes'''
    def __init__(self, title='', name='', taxid=0, factor='', age='',diet='',gene='',strain='',tissue='', cell_type='', intervention='',
                 type=None, genotype='', sex='', method='', mark=None, process=None, control=None):
        dict.__init__(self)
        self.title = title
        self.name = name
        self.taxid = int(taxid)
        self.type = type  # Can be profile, dataset, meta or series.

        self.age = age
        self.strain = strain
        self.tissue = tissue
        self.type = type
        self.diet = diet
        self.gene = gene
        self.genotype = genotype
        self.method = method
        self.factor = factor
        self.sex = sex
        self.intervention = intervention
        self.mark = mark
        self.process = process
        self.control = control
        
        self.genes = {}
        
        self.cutoff = 5.0
        self.delta = {}
        self.up = {}   
        self.down = {}

    def combine(self, S):
        self.name = self.name + S.name
        for gene in S.genes:
            if gene in self.genes:
                self.genes[gene] = S.genes[gene]#self.genes[gene].merge()
                print type(self.genes[gene])
##                print "merging", gene, self.genes[gene].fold_change
            else:
                print "adding", gene, S.genes[gene].fold_change
                self.genes[gene] = S.genes[gene]

    def expression(self, ratio=2.0, pvalue=None):
        """ """
        if self.delta:
            self.delta = {}
            self.up = {}
            self.down = {}
        if not pvalue:
            for id, gene in self.items():
                if gene.ratio >= ratio:
                   self.up[id] = gene
                   self.delta[id] = gene
                elif gene.ratio and gene.ratio <= 1/ratio:
                    self.down[id] = gene
                    self.delta[id] = gene
        else:
            for id, gene in self.items():
                if gene.pvalue < pvalue:
                    if gene.ratio >= ratio:
                       self.up[id] = gene
                       self.delta[id] = gene
                    elif gene.ratio and gene.ratio <= 1/ratio:
                        self.down[id] = gene
                        self.delta[id] = gene
        return len(self.delta), len(self.up), len(self.down)

    def read(self, taxid=None, title=None, name=None, pathToFile=None):
        if taxid and title and not name: pass
           
    def __repr__(self):
        if not self.delta: self.expression()
        return "%s: %s %s %s" % (self.name, len(self.delta), len(self.up), len(self.down))

    def contrast(self, signatures):
        '''contrasts different signatures with each others.
        Takes up a list of signatures and creates new signatures.'''
        for nameA, signatureA in signatures.items():
            for nameB, signatureB in signatures.items():
                if signatureA.factor == 'diet' == signatureB.factor: pass
                    #signature = Signature(name = signatureA.genotypesignatureA.diet, signature, )                    
                DR = Data(genotype=signature.genotype, diet='DR')
                AL = Data(genotype=signature.genotype, diet='AL')
                
    def update_ratios(self):
        for id, gene in self.genes.items():
            gene.update_ratio()

    def pValues(self):
        """Triggers the calculation of p-values for each gene in the signature."""
        for gene in self:
            self[gene].pValue()

    def save(self, path=None, name=None):
        """Serialize the signature."""
        if not path: path = 'D:', 'signatures', 'shelve'
        if not name: name = self.name
        data = shelve.open(os.path.join(path, name))
        for id, gene in self.items():
            data[str(id)] = gene
        data.close()

    def load(self, path=None, name=None):
        """Desialize the signature."""
        if not path: path = 'D:', 'signatures', 'shelve' 
        if not name and self.name: name = self.name
        data = shelve.open(name)
        for id, gene in data:
            self[id] = gene
        data.close()
        
    def serialize(self):
        """Depreciated, use save() instead."""
        path = 'D:', 'signatures', 'shelve',self.name
        shelve.open(os.path.join(*path))

    def deserialize(self):
        """Depriciated, use load() instead."""
        path = 'D:', 'signatures', 'shelve', self.name
        self = shelve.open(os.path.join(*path))

    def annotate(self, filename):
        """Takes in a file name and annotates the signature."""
        f = filename.split('.txt')[0]
        attributes = f.split(';')
        for attribute in attributes:
            k, v = attribute.split('=')
            #print k,v
            exec("self."+k+"='"+v+"'")
        self.create(filename)

    def create(self, filename, printing=False, fc_ratio=True):
        """Creates the signature from a file.
        if fc_ratio is True fold changes will be used as ratios."""
        data = file(filename).read().split('\n')
        #for line in data: print line
        input = data
        taxid = self.taxid

       # Adds the genes to the signature:

       # Adds the genes to the signature:
        info = {}       #Provides a mapping of the header to fascilate gene info matching.
        c = 0
        for column in input[0].split('\t'):
            if fc_ratio:
                column = column.replace('Fold change', 'ratio')
            info[c] = column.lower().replace(' ', '_')
            if info[c] in Gene.mapping: info[c] = Gene.mapping[info[c]]
            if info[c] not in Gene.keys: print '...', info[c]#, "Warning! Could not recoqnise: ", 
            c += 1
            
        L = len(input); n = 0; PB = 0 # Start Counter

        for i in input:
            
            n += 1; PA = 100*n/L # Continue Counter
            if PA != PB and printing: print PA,
            PB = PA
            
            if i == input[0] or not i:
                continue
            i = i.replace('"', '')  #Cleans up all the Excel inserted " strings marks.



            columns = i.split('\t')
            gene_info = []
        
            c = 0

            fold_change = []
            ratio = []
            
            for column in columns:
                if column and column not in ['#N/A', '#DIV/0!'] and c in info:

                    # Determine whether it is a an integer, float or string:
                    try:
                        if column == "nan" and info[c] == "gene_symbol": mapping = '"'+column+'"'
                        elif "." in column: mapping = str(float(column))
                        else: mapping = str(int(column))
                    except:
                        mapping = '"'+column+'"'
                        mapping = mapping.replace('\xa0','')

                    if info[c] in Gene.mapping:
                        info[c] = Gene.mapping[info[c]]
                    if info[c] in Gene.keys:
                        gene_info.append(info[c]+'='+mapping)
##                                    else: print "Couldn't recoqnise: ", info[c], S.name, S.title
                        #print gene_info

                    # If multiple fold_changes are giving average them
                    if "fold_change" in info[c] and info[c] != "fold_change" and mapping:
                        fold_change.append(float(mapping))

                    if "ratio" in info[c] and info[c] != "ratio" and mapping:
                        ratio.append(float(mapping))
                        
                c += 1
                
            if fold_change != [] and 'fold_change' not in "".join(gene_info):
                fold_change = sum(fold_change)/len(fold_change)    
                gene_info.append('fold_change='+mapping)
                
            if ratio != [] and 'ratio' not in "".join(gene_info):
##                                ratios = ratio
##                                print ratios
                ratio = sum(ratio)/len(ratio)    
                gene_info.append('ratio='+mapping)
            
            # Write an extre method which calculates the differential expression statistics
            # from the data supplied to a signature. Call method just before seriliziation
                
            if 'taxid' in ' '.join(info.values()):  # http://stackoverflow.com/questions/2536625/how-do-i-join-the-values-of-nested-python-dictionary
                G = eval('Gene('+", ".join(gene_info)+')')
            else:
                G = eval('Gene('+", ".join(list(set(gene_info)))+', taxid='+str(taxid)+')')
                
            #G.alsoKnownAs()
            #if not G.id: G.id = m(map(str, G.aka), int(taxid))[0]  #Deactive if prociding should be without mapping
            #if G.ensembl_gene == '': G.ensembl_gene = m(map(str, G.alias), int(taxid))[1]['ensembl_gene']
            #if G.ensembl_gene and G.ensembl_gene not in S: S[G.ensembl_gene[0]] = G #print "Couldn't map ", G.alias
            #if G.id and G.id not in S: S[G.id] = G
            #elif G.id and G.id in S: S[G.id].merge(G) # Does it actually work?
            #elif G.ensembl_gene: S[G.ensembl_gene[0]] = G #print "Couldn't map ", G.alias len(G.ensembl_gene) >=1
            #G.aka = []
            G.id = G.ensembl_gene or G.ensembl_transcript[0]
            self[G.id] = G

    def top(self, dir='up', limit=300):
        """Retrievies the top differential expressed genes."""
        ratios = []
        for id, gene in self.items():
            ratios.append((gene.ratio, gene))
        ratios.sort()
        results = [gene for (ratio, gene)  in ratios]
        if dir == 'up':
            for index, gene in enumerate(results):
                print("%s\t%s" % (gene.id, gene.ratio))
                if index == limit:
                    break
        else:
            results_reverted = results.reverse()
            for index, gene in enumerate(results):
                print("%s\t%s" % (gene.id, gene.ratio))
                if index == limit:
                    break
        return results


def germline(signatures):
    signatures.search(name='Young adult gonad')         #;factor=tissue;tissue=gonad;type=profile;method=tiling array')
    signatures.search(name='Germline expressed')  #;factor=tissue;type=profile;method=SAGE')
    signatures.search(name='Germline specific')   #;factor=tissue;type=profile;method=SAGE')
    signatures.search(name='Germline intrinsic')
    for signature in signatures:
        print signature, len(signatures[signature])

signatures = Signatures()  
if __name__ == '__main__':
    signatures = germline(Signatures()) 

