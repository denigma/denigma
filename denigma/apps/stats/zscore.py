"""Modules that calculutes the z-scores for e.g. microarray data.
It deals correctly with nan values.

Data from a Microarray experiment need be put into an array prior
and then likely normalize the data.

Inspired by: http://telliott99.blogspot.de/2010/01/z-scores.html

Depriciated, there is not yet any not for this module.""" 
from numpy import nan, isnan
from numpy import array, mean, std, random

def z_score(row):
    L = [n for n in row if not isnan(n)]
    m = mean(L)
    s = std(L)
    zL = [1.0 * (n - m) / s for n in L]
    if len(L) == len(row): return zL
    # deal with nan
    retL = list()
    for n in row:
        if isnan(n):
            retL.append(nan)
        else:
            retL.append(zL.pop(0))
    assert len(zL) == 0
    return retL

def z_score_by_row(A):
    retL = [z_score(r) for r in A]
    Z = array(retL)
    Z.shape = A.shape
    return Z


# utilies:

def show(row):
    m = mean(row)
    s = std(row)
    print row
    print('mean {} stdev {}'.format(round(m,4), round(s,4)))
    zL = (row - m) / s
    print(zL)

def has_nan(row):
    for n in row:
        if isnan(n): return True
    return False

if __name__ == '__main__':
    random.seed(137)
    N = 10000
    A = random.randn(N)
    A *= 10
    for i in range(20):
        A[random.randint(N)] = nan
    A.shape = (2500, 4)

    Z = z_score_by_row(A)

    for i in range(2):
        j = random.randint(1000)
        # print(j)
        show(A[j])
        print(Z[j])
        print('')

    L = [(i,r) for i,r in enumerate(A) if has_nan(r)]
    for t in L[:2]:
        i = t[0]
        print(A[i])
        print(Z[i])
