"""Creates signatures from the age-1 micrarray analysis
# Create three profiles
# Populate the three profiles
# Calculate the average and variance for each gene in each profile
# Generate signatures by calculating all the contrasts:
#   exp='mg44', ctr='N2'
#   exp='m333', ctr='N2'
#   exp='mg44', ctr='m333'
# invoke signature statics function to calculate the p-values
# invoke expression to calculate the differentially expressed genes, either with or without signatures
#   maybe doing this for a spectrum on fold-changes.
"""

from signature import *
from gen import *
from stats.pValue import ttest


class Data():
    def __init__(self):
        pass


class Profiles(dict):
    """A collection of molecular profiles (i.e. a set of gene lists) with names."""
    def __init__(self, groups=None, taxid=None, method=None):
        dict.__init__(self)
        if groups:
            for group in groups:
                self[group] = Profile(name=group, taxid=taxid, method=method)

    def expression(self):
        """Calculates the average expression of each gene in each profile."""
        for profile in self:
            profiles[profile].expression()

    def variance(self):
        """Calcululates the varianc of expression of each gene in each profile."""
        for profile in self:
            self[profile].variance()

    def add(self, profile):
        """Adds another profiles to the collection of profiles.
        Requires a unique name for the new profile for adding."""
        self[profile.name] = profile

    def signing(self, exp=None, ctr=None):
        """It takes two profiles as experimental and control set, respectively
        and generates a signature by contrasting them.
        Assumes profiles are from same species."""
        signature = Signature(name="%s vs. %s" % (self[exp].name, self[ctr].name), taxid=self[exp].taxid )
        for gene in self[exp]:
            signature[gene] = self[exp][gene] + self[ctr][gene]
            try: signature[gene].ratio = self[exp][gene].expression / self[ctr][gene].expression
            except TypeError:
                #print "Encontered an TypeError:"
                #print self[exp][gene], '\n'
                #print self[ctr][gene], '\n'
                pass
            except ZeroDivisionError:
                #print "Econtered an ZeroDivisionError:"
                #print self[exp][gene], '\n'
                #print self[ctr][gene], '\n'
                pass
            try: signature[gene].pvalue = ttest(self[exp][gene].expressions, self[ctr][gene].expressions)
            except ZeroDivisionError: signature[gene].pvalue = 0 # What to do here?
            signature[gene].exp_variance = self[exp][gene].variance
            #signature[gene].ctr_variance = self[ctr][gene].variance
            signature[gene].exp = self[exp][gene].expressions
            signature[gene].ctr = self[ctr][gene].expressions
        return signature

    def profiling(self):
        for profile in self:
            print profile, len(self[profile])
            for gene in self[profile]:
                print gene, self[profile][gene].expression, self[profile][gene].variance


class Profile(dict):
    """A moleculare profile (i.e. gene lists with expression values)."""
    def __init__(self, name=None, taxid=None, method=None):
        dict.__init__(self)
        self.name = name
        self.taxid = taxid
        self.method = method
##        probe_id
##        entrez_gene_id
##        mapping
##        exp
##        ctr
##        fold_change
##        taxid
##        condition
##        age
##        mutant,
##        strain

    def expression(self):
        """Calculates the average expression of each gene in the profile."""
        for gene in self:
            self[gene].averageExpression()
      
    def variance(self):
        """Computes the variances of each gene expression."""
        for gene in self:
            self[gene].calcVariance()

    def __add__(self, profile):
        """Adds the the genes of two profiles together."""
        newProfile = Profile('%s+%s' % (self.name, profile.name), taxid=self.taxid)
        for gene in profile:
            if gene in self:
                newProfile[gene] = self[gene] + profile[gene]
        return newProfile


def pi3k(signatures):
    profiles = Profiles(groups=['mg44', 'm333', 'hx546', 'N2'], taxid=6239, method='DNA-microarray')

    D = {}
    path = 'D:/signatures/6239/age-1/'
    files = ['mg44+m333 vs hx546', 'mg44+m333 vs N2']
    for f in files:
        Input = file(path+f+'.txt').read().split('\n')
        for line in Input:
            s = line.split('\t')
            if line == Input[0] or s[0] == '': continue
            elif s[0] == 'ch1-Cy3; ch2=Cy5':
                header = {}
                for x in xrange(0,len(s)):
                    header[x] = s[x]
                continue
            D[s[0]] = D.get(s[0],{'mg44':[], 'm333':[], 'hx546':[], 'N2':[]})
            for profile in profiles:
                profiles[profile][s[0]] = profiles[profile].get(s[0], Gene(ensembl_gene=s[0]))
            for x in xrange(0, len(s)):
                try:
                    D[s[0]][header[x]].append(int(s[x]))
                    profiles[header[x]][s[0]].expressions.append(int(s[x]))
                except: pass

    profiles.variance()                                                     # Variance
    profiles.add(profiles['mg44']       + profiles['m333'])
    profiles.add(profiles['mg44+m333']  + profiles['hx546'])
    #signatures = Signatures(name='age-1')
    signatures.add(profiles.signing(exp='mg44',             ctr='N2'),
                   profiles.signing(exp='m333',             ctr='N2'),
                   profiles.signing(exp='mg44+m333',        ctr='N2'),
                   profiles.signing(exp='hx546',            ctr='N2'),
                   profiles.signing(exp='mg44+m333+hx546',  ctr='N2'),
                   profiles.signing(exp='mg44',             ctr='hx546'),
                   profiles.signing(exp='m333',             ctr='hx546'),
                   profiles.signing(exp='mg44+m333',        ctr='hx546'))

    print signatures

    return signatures, profiles

##for signature in signatures:
##    print signature

if __name__ == '__main__':
    signatures = Signatures()
    germline(signatures)
    signatures, profiles = pi3k(signatures)
