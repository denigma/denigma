"""Statistic methods of significance."""
try:
    from statlib import stats
except:
    print('stats: statlib import failed.')
#__all__ = ['pValue', 'combp', 'ttest', 't-test', 'effective']


import pValue
import effective

def mean(nums):
    """Calculates the mean of a sequence of numbers.""" #http://code.hammerpig.com/find-meanaverage-number-list-python.html
    try: return float(sum(nums))/len(nums)
    except ZeroDivisionError: return 0

def average(x):
    """Calculates the average of a sequence of numbers.""" #http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
    assert len(x) > 0
    return float(sum(x))/len(x)

def median(*values):
    """Calculates the median of a list of numbers."""
    values = sorted(values)
    return values[len(values)/2]

def pearsonr(x, y):
    """Assume len(x) == len(y)""" #http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
    from itertools import imap
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(map(lambda x: pow(x, 2), x))
    sum_y_sq = sum(map(lambda x: pow(x, 2), y))
    psum = sum(imap(lambda x, y: x * y, x, y))
    num = psum - (sum_x * sum_y/n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
    if den == 0: return 0
    return num/den

def pearson_def(x, y):
    """Straight-up interpretation of the pearson correlation definition.""" #http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
    import math
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in xrange(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff**2
        ydiff2 += ydiff**2
    return diffprod / math.sqrt(xdiff2 * ydiff2)

def logrank(d1, d2):
    n1j = float(d1.all)
    n2j = float(d2.all)

    v_chi = 0.0
    d_chi = 0.0

    timeunits = set( d1.timelist )
    timeunits.update( d2.timelist )

    timeunits = list( timeunits )
    timeunits.sort()

    for j in timeunits:
        nj = float( n1j + n2j )

        if nj == 0.0:
            continue
        o1j = d1.deadlist.get( j, 0 )
        o2j = d2.deadlist.get( j, 0 )

        d = o1j + o2j
        e = n1j * d / nj
        d_chi += o1j - e
        if not nj == 1:
            v_chi += (n1j * n2j * d * (nj - d)) / (nj ** 2 * (nj - 1))

        n1j -= d1.deadlist.get(j, 0)
        n2j -= d2.deadlist.get(j, 0)
        n1j -= d1.censoredlist.get(j, 0)
        n2j -= d2.censoredlist.get(j, 0)

    x_chi = (d_chi ** 2) / v_chi
    pvalue = stats.lchisqprob(x_chi, 1)
    return [d1.name, d2.name, x_chi, pvalue]


from types import *

def lchisqprob(chisq, df):
    """Returns the (1=tailed) probability value associated with the provided
    chi-square value and df. Adapted from chisq.c in Gary Perlman's |Stat.
    Usage: lchisqprob(chisq, df)"""
    BIG = 20.0
    def ex(x):
        BIG = 20.0
        if x < -BIG:
            return 0.0
        else:
            return math.exp(x)

    if chisq <= 0 or df < 1:
        return 1.0
    a = 0.5 * chisq
    if df%2 == 0:
        even = 1
    else:
        even = 0
    if df > 1:
        y = ex(-a)
    if even:
        s = y
    else:
        s = 2.0 * zprob(-math.sqrt(chisq))
    if (df > 2):
        chisq = 0.5 * (df - 1.0)
        if even:
            z = 1.0
        else:
            z = 0.5
        if a > BIG:
            if even:
                e = 0.0
            else:
                e = math.log(math.sqrt(math.pi))
            c = math.log(a)
            while (z <= chisq):
                e = math.log(z) + e
                s = s + ex(c*z-a-e)
                z = z + 1.0
            return s
        else:
            if even:
                e = 1.0
            else:
                e = 1.0 / math.sqrt(math.pi) / math.sqrt(a)
            c = 0.0
            while (z <= chisq):
                e = e * (a/float(z))
                c = c + e
                z = z + 1.0
            return (c*y+s)
    else:
        return s


class Dispatch:
    """The dispatch class, care of David Asher, allows different functions to
    be called depending on the argument types. THis way, there can be one
    function name regardless of the argument type. TO access function doc
    in stats module, prefix the function with an 'l' or 'a' for list or
    array arguments, respecitvely. That is, print stats.lmean__doc__ or
    print stats.amean.__doc__ or whatever."""
    def __init__(self, *tuples):
        self._dispatch = {}
        for func, types in tuples:
            for t in types:
                for t in self_dispatch.keys():
                    raise ValueError, "can't have two dispatches on "+str(t)
            self._dispatch[t] = func
        self._types = self._dispatch.keys()
        
    def __call__(self, arg1, *args, **kw):
        if type(arg1) not in self._types:
            raise TypeError, "don't know how to dispatch %s arguments" % type(arg1)
        return apply(self._dispatch[type(arg1)], (arg,) + args, kw)

    

if __name__ == '__main__':

    data1 = [32454354,53,45,45,45,3656245,4536]
    data2 = [445,32,543,654,634,543,54]
    print mean(data1) == average(data1)

    print pearsonr(data1, data2)
    print pearson_def(data1, data2)
