"""A module to Combine p-values."""
import math
try:
    import numpy as np
    _NUMPY = True
except:
    print('Warning NumPy not found. Get it: http://numpy.scipy.org/ or http://www.lfd.uci.edu/~gohlke/pythonlibs/ or $easy_install scipy or $pip install scipy')
    _NUMPY = False
try:
    import scipy.stats
    _SCIPY = True
except:
    print('Warning SciPy not found. Get it: http://www.scipy.org/ or http://www.lfd.uci.edu/~gohlke/pythonlibs/ or $easy_install numpy or $ pip install numpy')
    _SCIPY = False

import decimal
#from stats.superfloat import SuperFloat, sfloat

#234567891123456789212345678931234567894123456789512345678961234567897123456789

_TINY = 1e-15

def zscore(pvalue):
    """Return the z-score corresponding to a given p-value."""
    pvalue = np.minimum(np.maximum(pvalue, _TINY), 1.-_TINY)
    z = scipy.stats.norm.isf(pvalue)
    return z

def combsp(pvalues):
    """A simple method to assess the overal significance.""" # http://www.loujost.com/Statistics%20and%20Physics/Significance%20Levels/CombiningPValues.htm
    try:
        k = 1.
        for pvalue in pvalues:
            k = k * pvalue
        p = k - (k * math.log(k))
    except ValueError:
        k = decimal.Decimal('1.')
        for pvalue in pvalues:
            k = k * decimal.Decimal(pvalue)
        p = k - (k * k.log10())
    return p

def combfp(pvalues):
    """Fisher's method of combining p-values.""" #http://mikelove.wordpress.com/category/statistics/
    return 1 - scipy.stats.chi2.cdf(-2 * sum(math.log(p) for p in pvalues), 2*len(pvalues))

def comb2p(p1, p2):
    """Combines 2 p-values.

    Let p1 and p2 be the p-values form dataset 1 and dataset 2.
    Under the null hypothesis both p-values are distributed uniformly in [0,1].
    If we assme independence then the probility that their product is less than x equals x - x*log(x)
    (where log is the natural - base e - logarithm).""" #http://permalink.gmane.org/gmane.science.biology.informatics.conductor/32378

    return p1 * p2 - p1 * p2 * math.log(p1 * p2)

def combnp(pvalues):
    """Combines n p-values together.""" #http://permalink.gmane.org/gmane.science.biology.informatics.conductor/32378
    allp = 1.
    for p in pvalues:
        allp *= p
    return allp - allp * math.log(allp)

def combzp(pValues):
    """Combines p-values via the z-method.""" #http://permalink.gmane.org/gmane.science.biology.informatics.conductor/32378
    zScores = []
    for pValue in pValues:
        zScore = zscore(pValue)
        zScores.append(zScore)
    zScoreCombined = 0
    for zScore in zScores:
        zScoreCombined += zScore
    zScoreCombined = zScoreCombined / (math.sqrt(len(pValues)))
    return scipy.stats.norm.sf(zScoreCombined)#*2 # Return one-s http://stackoverflow.com/questions/3496656/convert-z-score-z-value-standard-score-to-p-value-for-normal-distribution-in


def zmethod(pValues):
    """Z transform method.
    Alternative method for combining p-vlaues from n independent tests,
    with being sperior to Fisher's method (Whitlock 2005).
    Here, the unweigthened Z-transform is applied,
    which is analogous to the probit transformation.
    Each p-values is transformed into a normal deviate
    via the normal probability transformation, that is z = psi^-1(p),
    where psi is the nromal probaility distribution function.
    The sum S = sum(zScores) has a normal distribution with mean 0 and variance n,
    so that S/sqrt(n) has again a normal N(0,1) distribution,
    from which the combined p-vlaue is computed
    as the normal distribution funntion associated with S/sqrt(n),
    that is, as p = psi[S!sqrt(n)].
    For example, the three p-values [0.011, 0.047, 0.35] result in
    a combined significance level of 0.006.
    Boundary values: For numerical reasions, an input smaller than
    the lower bound in the Fisher method is replaced by this lower bound.
    An input value larger than 0.9999999999999999999 will be replaced
    by this boundary value.
    Again, however, values of p ~ 0 and p ~ 1 will not generally yield
    reasonable results""" # http://linkage.rockefeller.edu/ott/util.htm#pvalues
    zScores = [zscore(pValue) for pValue in pValues]
    return scipy.stats.norm.sf(sum(zScores) / (math.sqrt(len(pValues))))
               

def test(pvalues=(0.05, 0.01, 0.0043, 0.0034)):
    """Tests p-value combinations functions.
    Takes a sequence of p-values and prints
    the result of all methods."""

    for pvalue in pvalues:
        try:
            print('zscore of {} is {}'.format(pvalue, zscore(pvalue)))
        except:
            print('zscore could not be calculated. NumPy = {}; SciPy = {} '.format(_NUMPY, _SCIPY))
    print('combsp: {}'.format(combsp(pvalues)))
    print('combfp: {}'.format(combfp(pvalues)))
    try:
        print('comb2p: {}'.format(comb2p(*pvalues)))
    except:
        print('comb2p takes only two p-values! ' \
              'Result from the first two p-values: ' \
              '{}'.format(comb2p(*pvalues[:2])))
    print('combnp: {}'.format(combnp(pvalues)))
    try:
        print('combzp: {}'.format(combzp(pvalues)))
    except:
        print('combzp could not be calculated. NumPy = {}; SciPy = {} '.format(_NUMPY, _SCIPY))

if __name__ == '__main__':
    #print zscore(0.01)
    #print zscore(0.5)
    data = [0.011, 0.047, 0.35, 0.2]
    print combsp(data)
    print combzp(data)
    print zmethod(data)
    print combfp(data)
    #print combfp([0.01, 0,01])
    
    #test()
