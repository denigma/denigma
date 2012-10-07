"""A module full of statistical test to calculate significance, etc."""

### Calculate Exact Binomial Distribution Probility ###
import math
from math import *
from math import factorial

try:
    import scipy
    from scipy.stats import *
    from scipy import special
except ImportError as e:
    print("denigma.stats.pValue: Failed to import scipy. %s" % str(e))

import numpy

try:
    from cogent.maths.stats.test import t_two_sample
except ImportError as e:
    print("denigma.stats.pValue: %s" % str(e))


def factorial(n): 
    if n < 2: return 1
    return reduce(lambda x, y: x*y, xrange(2, int(n)+1))

def prob(s, p, n):
    x = 1.0 - p
    
    a = n - s
    b = s + 1

    c = a + b - 1.0

    probe = 0

    for j in xrange(int(a), int(c) + 1):
        probe += factorial(c) / (factorial(j)*factorial(c-j)) \
                * x**j * (1 - x)**(c-j)
    return probe


### Normal Estimate, good for large n ###

def erf(z):
    t = 1.0 / (1.0 + 0.5 * abs(z))
    # use Horner's method
    ans = 1 - t * math.exp(-z*z -  1.26551223 +
                            t * ( 1.00002368 +
                            t * ( 0.37409196 + 
                            t * ( 0.09678418 + 
                            t * (-0.18628806 + 
                            t * ( 0.27886807 + 
                            t * (-1.13520398 + 
                            t * ( 1.48851587 + 
                            t * (-0.82215223 + 
                            t * ( 0.17087277))))))))))
    if z >= 0.0:
            return ans
    else:
            return -ans

def normal_estimate(s, p, n):
    u = n * p
    o = (u * (1-p)) ** 0.5

    return 0.5 * (1 + erf((s-u)/(o*2**0.5)))

#Calculating p-value:
def B(n,k):
    if n > k:
        b = factorial(n) / (factorial(k)*factorial(n-k))
        return b
    
#p-value for intersection of two lists:
def hyperpvalue(n1,n2,n,m):
    '''len(Set1), len(Set2), n, len(overlap)'''
    x = B(n1, m)
    y = B((n-n1),(n2-m))
    z = B(n,n2)

    Stringx = str(x)
    Stringy = str(y)
    Stringz = str(z)

    FactorX = float(Stringx[0:5])/10000
    FactorY = float(Stringy[0:5])/10000
    FactorZ = float(Stringz[0:5])/10000

    VOrFactor = round(FactorX*FactorY/FactorZ,1)

    PotenzX = len(str(x))
    PotenzY = len(str(y))
    PotenzZ = len(str(z))

    NAchFactor = 10**(PotenzX+PotenzY-PotenzZ-1)

    Result = VOrFactor * NAchFactor

    return Result

def binom(n,m):
    b = [0] * (n + 1)
    b[0] = 1
    for i in xrange(1, n + 1):
        b[i] = 1
        j = i- 1
        while j > 0:
            b[j] += b[j - 1]
            j -= 1
    return b[m]

def calc_benjamini_hochberg_corrections(p_values, num_total_tests):     #http://stats.stackexchange.com/questions/870/multiple-hypothesis-testing-correction-with-benjamini-hochberg-p-values-or-q-va
    """
    Calculates the Benjamini-Hochberg correction for multiple hypothesis
    testing from a list of p-values *sorted in ascending order*.

    See
    http://en.wikipedia.org/wiki/False_discovery_rate#Independent_tests
    for more detail on the theory behind the correction.

    **NOTE:** This is a generator, not a function. It will yield values
    until all calculations have completed.

    :Parameters:
    - `p_values`: a list or iterable of p-values sorted in ascending
      order
    - `num_total_tests`: the total number of tests (p-values)

    Source: http://stats.stackexchange.com/questions/870/multiple-hypothesis-testing-correction-with-benjamini-hochberg-p-values-or-q-val
    """
    prev_bh_value = 0
    for i, p_value in enumerate(p_values):
        bh_value = p_value * num_total_tests / (i + 1)
        # Sometimes this correction can give values greater than 1,
        # so we set those values at 1
        bh_value = min(bh_value, 1)

        # To preserve monotonicity in the values, we take the
        # maximum of the previous value or this one, so that we
        # don't yield a value less than the previous.
        bh_value = max(bh_value, prev_bh_value)
        prev_bh_value = bh_value
        yield  p_value, bh_value


##                choose(r, x) * choose(b, n-x)
##p(x; r,b,n) = -----------------------------
##                choose(r+b, n)


##N = b +r      #Total number
##r = m         #Essential
##n             #sampleSize
##x    k      #intersection

##b = N - m



def logchoose(n, k):
    lgn1 = special.gammaln(n+1)
    lgk1 = special.gammaln(k+1)
    lgnk1 = special.gammaln(n-k+1)
    return lgn1 - (lgnk1 + lgk1)

def gauss_hypergeom(x, r, b, n):
    return exp(logchoose(r, x) + logchoose(b, n-x) - logchoose(r+b, n))

def hypergeom(x, r, b, n, e='enriched'):
    SumP = 0
    if e == 'enriched':
        for number in range(n):
            if number > x:
                result = exp(logchoose(r, number) + logchoose(b, n-number) - logchoose(r+b, n))
                #print number, result
                SumP += result
        return  SumP
    if e == 'depleted':
        for number in range(x):
            result = exp(logchoose(r, number) + logchoose(b, n-number) - logchoose(r+b, n))
            #print number, result
            SumP += result
        return  SumP        

def hyperg(set1, set2, total, overlap, e='enriched'):
    x = overlap
    r = set1
    b = total-set1
    n = set2
    SumP = 0
    if e == 'enriched':
        for number in range(n):
            if number > x:
                result = exp(logchoose(r, number) + logchoose(b, n-number) - logchoose(r+b, n))
                #print number, result
                SumP += result
        return  SumP
    if e == 'depleted':
        for number in range(x):
            result = exp(logchoose(r, number) + logchoose(b, n-number) - logchoose(r+b, n))
            #print number, result
            SumP += result
        return  SumP     

def poisson_probability(actual, mean): #http://stackoverflow.com/questions/280797/calculate-poisson-probability-percentage-in-python
    # naive:
    #p = math.exp(-mean) * mean**actual / factorial(actual)
    # iterative, to keep the components from getting too large or small:
    p = math.exp(-mean)
    for i in xrange(actual):
        p *= mean
        p /= i+1
    return p


def naiveVariance(data):
    """Calculates the naive variance by passing a list of values."""
    n = 0
    Sum = 0
    Sum_sqr = 0
 
    for x in data:
        n = n + 1
        Sum = Sum + x
        Sum_sqr = Sum_sqr + x*x
 
    mean = Sum/n
    variance = (Sum_sqr - Sum*mean)/(n - 1)
    return variance

def variance(values):
    """Calculates a variance of values."""
    mean = 1.*sum(values)/len(values)
    for i in values:
        variance = (mean-i)**2
    return variance

def ttest(a,b):
    mean_a = 1.*sum(a)/len(a)
    #print mean_a
    mean_b = 1.*sum(b)/len(b)
    #print mean_b
    SSA, SSB = 0, 0
    for i in a:
        SSA += 1.*(mean_a-i)**2
    for i in a:
        SSB += 1.*(mean_b-i)**2
    #print SSA, SSB
    pooled_variance = 1.*(SSA+SSB)/(len(a)+len(b)-2)
    #print pooled_variance 
    t = 1.*(mean_a-mean_b)/sqrt(pooled_variance/len(a)+pooled_variance/len(b))
    return t


if __name__ == "__main__":
    L = [[3,3,3,3,3,2], [1,2342,54324,235,23]]
    for l in L:
        print variance(l)
        print naiveVariance(l)


    s = '''0.582833043
0.005412472
0.818337646
0.885831843
1
1
1
0.348437074
0.267922977
0.513925013
0.999843485
1
0.005789229
0.68978553
0.015088835
0
1
0.373475565
0.533901605
0.770907779
0.477888398
0.509850771
0.168695112
0.005789229
1
1
0.035147463
0.027608495
0.509424182
0.502373187
4.64E-05
0.095339979
0.286959103
1
1
0.368567865
0.612513514
0.156552709
0.137717932
0.20638593
0.695434249
0.445728796
0.047971775
0.587823427
0.304681547
0.445728796
1
1
0.000256663
0.360255703
0.533901605
1
0.062298906
1
1
0.009190669
0.126260152
0.35839614
0.342420561
1
0.038894421
1
0.485888233
0
0.795144985
0.241007953
0.185718741
0.042665366
1
0.815770661
0.557326386
0.785572265
1
0.119425364
0.611846987
0.297657114
1
0.007621819
1
0.938954171
1
0.512540518
0
0
1
0.65125146
0.008161021
1
1
1
1
1
0.772573396
0.032127309
1
0.132607619
0
1
1
0.021220084
0.927691493
0.999732784
0.132607619
0.533901605
0.006171673
0.782456572
0.975954124
0.150741907
1
0.255343135
1
0.010949928
1
1
1
1
1
1
0.226171966
1
0.290867883
1
1
1
0.008170673
0.065967153
0.620426507
1
0.958530372
1
1
0.474475863
1
1
0.569547521
0.385313237
0.9094692
1
0.226171966
0.068644096
0.277693138
0.418524395
0.140953837
0.519093917
0
0.156262898
1
0.219961708
0.153620713
0.611846987
0.000131861
1
0.876257869
1
0.601677109
0.132607619
1
0
1
0.565800856
1
0.012866706
0.398007252
0.001273565
1
1
0.24395995
1
0
0.707659723
0.175755708
0.206579137
0.069504196
0.449425286
1
0.001269012
1
0.848052279
0.042665366
1
0.20638593
0.449425286
0.276018639
1
0.302496802
0.125365419
0.403480811
0.109670739
1
0.226171966
0
0.022255478
1
0.301488888
0.642456806
1
0.583680234
1
1
1
0.400124525
1
1
0.142509483
0.375955489
0.859372922
0.155978711
1
1
0.140938924
0.760774605
0.216959692
1
0.268860136
0.231306883
1
0.000192858
0.359783775
1
0.069953141
0.155978711
1
0.216959692
0.717620176
0.318010587
0.148962507
1
1
0.329758968
0.273067715
0.706650374
1
1
0
1
1
1
1
0.677226613
1
0.033038352
0.139211635
0.388340642
1
0.688864643
0.497946953
0.042665366
0.999852893
0.971320152
1
0.111801675
1
0.999510351
0.001233634
0.257105372
0.770907779
1
0.710889762
0.053043472
0.112335558
0.917618135
1
0.20638593
0.00588987
0.65447932
0.893901718
0.01680197
0.119683093
0.117608473
0.55304981
1
0.981609185
0.062885892
0.345984554
0.408346408
0.780965465
0.509424182
0.284589169
1
1
0
1
1
0.375955489
0.005412472
1
0.826590398
1
0.025358757
0.342604839
0.819908758
0.047971775
1
0.117608473
0.08810025
0.132607619
1
0.818065867
1
0.300636885
0.329758968
0.502185063
0.010881759
0.042593324
0.483652006
0.081214438
1
1
0.41233851
0.481213617
0.086829232
1
1
0.533901605
1
1
1
1
0
1
0.642836737
1
0.826994276
0.995556404
0.737021285
0.678659423
1
0.7605833
1
1
0.33089247
1
0.150335521
0.157420348
1
0.785572265
1
0.708043492
0.679394636
0.994305617
1'''
    s = map(float,s.split('\n'))
    #s = [0.03, 0.04, 0.02]


##        if i != "":
##            pass
####            print float(i)
##        else: print "EERRO"
    #print calc_benjamini_hochberg_corrections(s, len(s))


    pValues = dict(calc_benjamini_hochberg_corrections(s, 1500000))##    for i in s:

##from scipy.misc import comb
##
##def binomial_test(n, k):
##    '''Calculates binomial probability
##    '''
##    p = comb(n, k) * 0.5**k*0.5**(n-k)
##    return p


'''
Do DR-essential genes have a higher total number as expected by chance?

expected value = average of degree of all genes

expect = degree of all genes/number of all genes.

observed = degree of DR-essential genes/number of DR-essential genes.


number DR-essential genes, probility (expectd), observed
'''

