import p
from pygr import worldbase
from motif import *
from pygr import annotation, mapping, worldbase
from pygr import sqlgraph 
from C import *


class Species():
    def __init__(self, taxid, latin_name, common_name, name, genome_name):
        self.taxid = taxid
        self.latin_name = latin_name
        self.common_name = common_name
        self.name = name
        self.genome_name = genome_name
        self.genome_build = ''
    def __repr__(self):
        return self.name

species, Organisms = [(4932, 'Saccharomyces cerevisea', 'Budding yeast', 'Yeast', 'YEAST'),
(6239, 'Ceanoharbiditis elegans', 'Nematode', 'Worm', 'CAEEL'),
(7227, 'Drosophila melanogaster', 'Fruit fly', 'Fly', 'DROME'),
(10090, 'Mus musculus', 'House mouse', 'Mouse', 'MOUSE'),
(9606, 'Homo sapiens', 'Human', 'Human', 'HUMAN')], {}

for s in species: Organisms[s[0]] = Species(s[0], s[1], s[2], s[3], s[4])
for taxid, s in Organisms.items(): print s.name


class UCSCStrandDescr(object):
    def __get__(self, obj, objtype):
        if obj.strand == '+':
            return 1
        else:
            return -1


class UCSCSeqIntervalRow(sqlgraph.TupleO):
    orientation = UCSCStrandDescr()

##from pygr import seqdb
##from pygr import cnestedlist
##yeast = seqdb.BlastDB('sacCer1')
##
##def create_annots():
##    for line in open('sgdGene.txt'):
##        info = line.split()
##        name = info[0]
##        seq = info[1]
##        if info[2] == '+':
##            strand = +1
##        else:
##            strand = -1
##        start = int(info[3])
##        stop = int(info[4])
##
##        yield name, (seq, mane, start, stop, strand)


class Genome():
    def __init__(self, O):
        self.species = O
        dir(worldbase.Bio.Seq)
        dir(worldbase.Bio.Seq.Genome)
        Genome = eval ('dir(worldbase.Bio.Seq.Genome.'+O.genome_name+')[-1]')
        O.genome_build = Genome


        serverInfo = sqlgraph.DBServerInfo(host='genome-mysql.cse.ucsc.edu', user='genome')
        txInfo = sqlgraph.SQLTable(O.genome_build+'.ensGene', serverInfo=serverInfo, itemClass=UCSCSeqIntervalRow, primaryKey='name')
        self.chromosome = eval('worldbase.Bio.Seq.Genome.'+O.genome_name+'.'+Genome+'(download=True)')
        for i in self.chromosome:
            print i, len(self.chromosome[i])
        self.annodb = annotation.AnnotationDB(txInfo, self.chromosome, sliceAttrDict=dict(id='chrom', start='txStart', stop='txEnd'))

##        self.gene_annots = dict(create_annots())
##        self.annot_db = seqdb.AnnotationDB(self.gene_annots, yeast, sliceAttrDict=dict(id=0, name=1, start=2, stop=3, strand-4))
##        self.annot_map = cnestedlist.NLMSA('genes', mode='memory', pairwiseMode=True)
##        for v in self.annot_db.values():
##            self.annot_map.addAnnotation(v)
##        self.annot_map.build()


'''Searches each genome'''
def FindTargets():
    for taxid, O in Organisms.items():
        print taxid, O
        if taxid == 10090:
            G = Genome(O)
            R = SearchGenome(G)

    print "loaded Genome"

    for motif, info in motifs.items():
        print motif, len(info)
        
    for motif in motifs['AAACYKTGGA']:#YGNCACAAAA']:
        if motif.closest_gene_distance < 800:
            print motif.closest_gene_distance, '\t', motif.closest_gene[3], '\t',
            print motif.upstream_gene_distance, '\t', motif.upstream_gene[3], '\t',
            print motif.downstream_gene_distance, '\t', motif.downstream_gene[3]

FindTargets()


def FindTF(Signature):
    O = Organisms[Signature.taxid]
    G = Genome(O)

Signatures = PickleIn('D:/Signatures/signatures.pkl')



##        Genomes = Genome = eval ('dir(worldbase.Bio.Seq.Genome.'+O.genome_name+')')
##        print Genomes
##        genes = sqlgraph.SQLTable(O.genome[genome_build], serverInfo=serverInfo, primaryKey='name')   # UCSC lacks a primary key, tehrefore name was assigned.


##            self.chromosomes[i] = self.genome[i]
##    chr7 = self.genome['chr7']
####    chr7 = seq.seqDict['sacCer1.chr7']
##    print len(chr7)
##    return chr7

##genes = sqlgraph.SQLTable(genome[genome_build], serverInfo=serverInfo, primaryKey='name')   # UCSC lacks a primary key, tehrefore name was assigned.
##print len(genes)
##print genes.columnName

##for g in G.annodb: print g, G.annodb[g].orientation
##
##for  taxid, O in Organisms.items():
##    if taxid == 4932:
##        G = Genome(O)
##        for name, chromosome in G.chromosomes.items():
####            if name == 'chr1':
##                #print type(chromosome)
##                R = SearchChr(str(chromosome))
'''Searches each chromsome'''
##for  taxid, O in Organisms.items():
##    if taxid == 4932:
##        G = Genome(O)
##        for name, chromosome in G.chromosomes.items():
##            if name == 'chr1':
##                #print type(chromosome)
##                R = SearchChr(str(chromosome))

##stop
##
##
##
##
##
##
##
##
##
##'''
##for chr in genome:
##
##class motif():
##    match = score
##    conservation = score
##    binding = score
##    closest_gene = gene
##    distance_to_tss = score
##    overal = sum_score
##    
##class gene():
##    number_sites = score
##    distance_to_tss = score
##    expression = score
##    overal = sum_score
##
##class Gene():
##    entrez_gene_id
##    ensembl_gene_id
##
### Network of symbols, names and ids. Nodes are symbols/names/ids and mappings are the edges.
##'''
##def MSA():
##    dir(worldbase)
##    dir(worldbase.Bio)
##    dir(worldbase.Bio.MSA)
##    dir(worldbase.Bio.MSA.UCSC)
##    worldbase.dir('Bio.MSA.UCSC.hg18_multiz17way', asDict=True)
##    msa = worldbase.Bio.MSA.UCSC.hg18_multiz17way()
##    chr1 = msa.seqDict['hg18.chr1']
##    mydict = ~(msa.seqDict)
##    mydict[chr1]
##    ival=chr1[10000:11000]
##    myslice = msa[ival]
##    for src,dest,e in myslice.edges():
##        print '%s %s\n%s %s %2.1f\n' % (str(src),mydict[src],str(dest),mydict[dest],e.pIdentity()*100.)
##        
##
##
####chr7 = Seq()
####
####s = chr7[157900:159102]
####from Bio.Seq import Seq
####from Bio.Alphabet import IUPAC
####cDNA = Seq(str(s), IUPAC.unambiguous_dna)
####Protein = cDNA.translate()
####print Protein
####
####
####s4 = chr7[156900:157912]
##
##
##
##from pygr.sequence import *
##def SeqOb():
##    '''Pygr Sequence Objects'''
##    s = Sequence('attatatgccactat', 'bobo') #Create a seqeunce named bobo
##    print s # interpreter will print repr(s)
##    t = s[-8:]
##    print t # interpreter will print repr(t)
##    print str(t)    # returns the sequence intervals as a string
##    print len(t)    # get seqeunce length
##    print t.start, t.stop, t.orientation
##    rc = -s # get the reverse complement
##    print str(rc[:5]) # its first five letters
##
##    '''Relations between seqeunces'''
##    print t.path
##    print t.path is t
##    print s.path is s
##    print t in s
##    print s[:3] < t
##    print s[3:5] + t # get enclosing interval
##    u = -t
##    print u
##    print u.path
##    print u.pathForward
##    '''Working with Sequnces form a FASTA File'''
##    from pygr import seqdb
##    sp = seqdb.SequenceFileDB('Fasta.txt')
##    print len(sp)
##    print sp.keys()
##    pagbo = sp['Seq3']
##    print len(pagbo)
##    print pagbo
##    t = pagbo[2:-3]
##    print len(t)
##    print t in s
##    print t in pagbo
##    print t.start, t.stop, t.orientation
##    print -t
##    print t.id
##    print t.db
##    print t.db is sp
##    idDict = ~sp
##    print idDict[t]
##    sp.close()
##
##    '''Working with Sequences from Worldbase'''
##    from pygr import worldbase
##    worldbase.dir('Bio.Seq.Genome.HUMAN')
##    hg17 = worldbase.Bio.Seq.Genome.HUMAN.hg17()
##    print len(hg17)
##    print hg17.keys()
##    chr1 = hg17['chr1']
##    print len(chr1)
##    s = chr1[100000000:100001000]
##    print len(s)
##    print repr(s)
##    print s
##
##    '''Pygr is Obsessed with Scalability'''
##    worldbase.dir()
##    print len(worldbase.dir())
##    
##
##    '''Accessing a Sequence Database over SQL'''
##    from pygr import sqlgraph
##    class UCSCmRNA(sqlgraph.RNASQLSequence):
##        'interprete row objects as seqeunce object a la knownGeneMrna'
##        def __len__(self): # get length by running SQL query
##            return self._select('length(seq)') # SQL SELECT expression
##    serverInfo = sqlgraph.DBServerInfo(host='genome-mysql.cse.ucsc.edu',
##                                      user='genome')
##    mrna = sqlgraph.SQLTableNoCache('hg18.knownGeneMrna', serverInfo=serverInfo,
##                             itemClass=UCSCmRNA,
##                             itemSliceClass=seqdb.SeqDBSlice)
##    print len(mrna)
##    s = mrna['uc009vjh.1']
##    print len(s)
##    #print s
##    t = s[100:210]
##    print t
##    print -t
##    serverInfo.close()
##
##    '''Plugging in Your Own Seqeunce Parser'''
##    import csv
##    def read_csv(ifile, filename):
##        'assume 1st col is id, 2nd is sequence'
##        class seqholder(object):
##            def __init__(self, id, sequence):
##                (self.id, self.sequence, self.length) = (id, sequence, len(sequence))
##        for row in csv.reader(ifile):
##            yield seqholder(row[0], row[1])
##    myseqs = seqdb.SequenceFileDB('someseqs.csv',reader=read_csv)
##    print len(myseqs)
##    print myseqs.keys()
##    foo = myseqs['foo']
##    print len(foo)
##    print foo
##    mysqs.close()
##
##    '''Combining Sequence Databases Using PrefixUnionDict'''
##    mm8 = worldbase.Bio.Seq.Genome.MOUSE.mm8()
##    rn4 = worldbase.Bio.Seq.Genome.RAT.rn4()
##    pud = seqdb.PrefixUnionDict(dict(hg17=hg17, mm8=mm8, rn4=rn4))
##    print len(pud)
##    print len(hg17) + len(rn4) + len(mm8)
##    print pud.keys()
##    idDict = ~pud
##    print idDict[chr1]
##    mouse_chr5 = pud['mm8.chr5']
##    print idDict[mouse_chr5]
##
##
##    from slice_pickle_obj import MySliceInfo
##    seq_id = 'gi|171854975|dbj|AB364477.1|'
##    slice1 = MySliceInfo(seq_id, 0, 50, +1)
##    slice2 = MySliceInfo(seq_id, 300, 400, -1)
##    slice_db = dict(A=slice1, B=slice2)
##
##    #Open sequence database and create annotation database object
##    from pygr import seqdb, annotation
##    dna_db = seqdb.SequenceFileDB('hbb1_mouse.fa')
##    annodb = annotation.AnnotationDB(slice_db, dna_db)
##    annodb.keys()
##    a = annodb['A']
##    len(a)
##    s = a.sequence
##    print repr(s), str(s)
##
##
##    from pygr import mapping
##    slice_db = mapping.Collection(filename='myshelve', mode='c')
##    slice_db['A'] = slice1
##    slice_db['B'] = slice2
##    slice_db.close()
##
##    slice_db = mapping.Collection(filename='myshelve', mode='r')
##    annodb = annotation.AnnotationDB(slice_db, dna_db)
##    for k in annodb:
##        print repr(annodb[k]), repr(annodb[k].sequence)
##
##'''Accessing SQL Databases'''
##from pygr import sqlgraph
##serverInfo = sqlgraph.DBServerInfo(host='genome-mysql.cse.ucsc.edu', user='genome')        
##genes = sqlgraph.SQLTable('hg18.knownGene', serverInfo=serverInfo,
##                          primaryKey='name')
##print len(genes)
##print genes.columnName
##print genes.primary_key
##tx = genes['uc009vjh.1']
##print tx.chrom
##print tx.txStart
##print tx.txEnd
##print tx.strand
##
##'''Customzing SQL Database Access'''
##class UCSCStrandDescr(object):
##    def __get__(self, obj, objtype):
##        if obj.strand == '+':
##            return 1
##        else:
##            return -1
##        
###Create  a subclass
##class UCSCSeqIntervalRow(sqlgraph.TupleO):
##    orientation = UCSCStrandDescr()
##
##
##txInfo = sqlgraph.SQLTable('hg18.knownGene', serverInfo=serverInfo, itemClass=UCSCSeqIntervalRow,
##                           primaryKey='name')
##tx = txInfo['uc009vjh.1']
##print tx.orientation
##
##
##from pygr import worldbase
##hg18 = worldbase.Bio.Seq.Genome.HUMAN.hg18()
##annodb = annotation.AnnotationDB(txInfo, hg18,
##                                 sliceAttrDict=
##                                 dict(id='chrom', start='txStart', stop='txEnd'))
##gene = annodb['uc009vjh.1']
##print repr(gene.sequence), gene.sequence
##
##
##'''Saving Data to a SQL Database'''
##liteserver = sqlgraph.SQLiteServerInfo('slicedb.sqlite')
##txInfo = sqlgraph.SQLTable('annotations', serverInfo=liteserver,
##                           writeable=True,
##                           createTable='CREATE TABLE annotations (k INTEGER PRIMARY KEY, seq_id TEXT, start INT, orientation INT);')
##txInfo.new(k=0, seq_id='gi|171854975|dbj|AB364477.1|', start=0, stop=50, orientation=1)
##txInfo.new(k=1, seq_id='gi|171854975|dbj|AB364477.1|', start=300, stop=400, orientation=-1)
##
##print len(txInfo)
##print txInfo.keys()
##
##annodb = annotation.AnnotationDB(txInfo, dna_db,
##                                sliceAttrDict=dict(id='seq_id'))
##print len(annodb)
##a = annodb[0]
##print len(a)
##print a.sequence
##a = annodb[1]
##print a.sequence
##liteserver.close()
##
####if __name__ == '__main__':
####    SeqOb()
##
##from pygr.sequence import *
##s = Sequence('attatatgccactat', 'Cabal') # Create a sequence named Cabal
##print s # interpreter will print repr(s)
