"""SNP handling module."""
import os
import fileinput


class SNPs(dict):
    """A collection of SNPs"""
    def __init__(self):
        pass

    def load(self, snpType, near):
        path = 'D:/Annotations/dbSNP/'
        filename = os.path.join(path, 'miRNA-%sSNPs-%s.txt' % (snpType, near))
        #o.write('SNP_name\tchr\tSNP_start\tSNP_stop\trefUCSC\tobserved\tmiRNA_ID\tmiRNA_ACC\tstart\tstop\tstrand\tregion\n')#\tscore\trefNCBI
        for line in fileinput.input([filename]):
            #if line == "": continue
            s = line.split('\t')
            #print s
            if len(s) < 5 or s[0] == '#bin' or s[0] == 'SNP_name': continue
            elif '_' in s[1]: continue
            #print  s
            snp = SNP(name=s[0], chr=s[1], start=s[2], stop=s[3], refUCSC=s[4], observed=s[5], acc=s[6], id=s[7], strand=s[10], region=s[11])  #refNCBI=s[7],score=s[5],  , save=snps
            self[snp.name] = snp
        #return snps


class SNP:
    """A small nuclear polymorphism."""
    #__slots__ = ['chr', 'start', 'stop', 'name', 'strand', 'refUCSC']    # 'score', refNCBI,  (Maybe consider to remove score and refUCSC) 
    def __init__(self, chr, start, stop, strand, refUCSC ,observed, save=False, name=None, id=None, acc=None, region=None):  # score, ,  refNCBI
        self.chr = chr.replace('chr', '')
        self.start = int(start)
        self.stop = int(stop)
        self.name = name
        #self.score = int(score)
        if strand == '+': self.strand = 1
        else: self.strand = -1
        #self.refNCBI = refNCBI
        self.refUCSC = refUCSC
        self.observed = observed
        self.id = id
        self.acc = acc
        self.region = region
        
        if isinstance(save, dict):
            if self.name not in save: save[self.name] = self
            else:
                #if '_' in save[self.name]
##                print "SNP already in snps!"
##                print save[self.name]
##                print
##                print self
##                print
                pass

    def __repr__(self):
        string = ''
        for k, v in vars(self).items():
            string += '%s = %s\n' % (k, v) 
        return string
            #print '\n'.join(self.name, refNCBI, self.observed, self.chr, self.start, self.stop, self.strand)

