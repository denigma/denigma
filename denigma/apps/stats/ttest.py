"""Harbours varios flavors of t-tests."""#http://telliott99.blogspot.com/2010/11/students-t-test-again-5.html
from __future__ import division
import numpy as np
from scipy.special import stdtr
from utils import unbiased_var as var
from utils import unbiased_std as std

def one_sample_t(A,mu):
    n = len(A)
    df = n-1
    z = (np.mean(A) - mu) / std(A)
    t = z * np.sqrt(n)
    return t, stdtr(df,t)

def paired_t(A,B,expected_diff=0):
    return one_sample_t(A - B,expected_diff)

def two_sample_t(A,B,expected_diff=0):
    diff = (np.mean(A) - np.mean(B) - expected_diff)
    na = len(A)
    nb = len(B)
    df = na + nb - 2
    sum_sq = (var(A)*(na-1) + var(B)*(nb-1))
    f = (1/na + 1/nb)/df
    t = diff/np.sqrt(sum_sq*f)  
    return (t, stdtr(df,t))
#==========================================
def test(func,D):
    if func == one_sample_t:
        result = one_sample_t(D['X'],D['mu'])
    elif func == paired_t:
        result = paired_t(D['X'],D['Y'])
    elif func == two_sample_t:
        result = two_sample_t(D['X'],D['Y'])
    if D['verbose']:
        print '%5.3f         %5.3f' % result
    return result

def t(a,b):
    A = np.array(a)
    B = np.array(b)
    result = test(two_sample_t,{'X':A,'Y':B,'verbose':False})
    return result

def t1(a,mu):
    A = np.array(a)
    result = test(one_sample_t,{'X':A,'mu':mu,'verbose':False})
    return result

def pt(a,b):
    A = np.array(a)
    B = np.array(b)
    result = paired_t(A,B)
    return result

if __name__ == '__main__':
    print 't-statistic  p-value'
    
    A = np.array([3.1,2.3,2.1,1.7])
    B = np.array([2.1,1.8,2.7,2.4])
    test(one_sample_t,{'X':A,'mu':3,'verbose':True})
    test(one_sample_t,{'X':B,'mu':3.5,'verbose':True})
    
    C = np.array([3.1,4.3,4.1,2.7])
    test(paired_t,{'X':A,'Y':C,'verbose':True})
    test(two_sample_t,{'X':A,'Y':C,'verbose':True})

    print '\ncep-1'
    N2 = np.array([0,  269, 547, 321,   1166,  752])
    AGE = np.array([2350, 1785, 9166, 8560, 353, 57])
    test(paired_t,{'X':AGE,'Y':N2,'verbose':True})
    test(two_sample_t,{'X':AGE,'Y':N2,'verbose':True})

    N2 = np.array([14317, 37960, 10044, 20323, 38620, 32643, 5418, 7608])
    AGE = np.array([848,136, 797, 295, 1733, 4016, 614, 984])
    test(paired_t,{'X':AGE,'Y':N2,'verbose':True})
    test(two_sample_t,{'X':AGE,'Y':N2,'verbose':True})
#9423	166933	176356	0.056447796



'''
R code:
A = c(3.1,2.3,2.1,1.7)
result = t.test(A, alternative='less',mu=3)
result$statistic
B = c(2.1,1.8,2.7,2.4)
result=t.test(B, alternative='less',mu=3.5)
result$statistic
C = c(3.1,4.3,4.1,2.7)
result=t.test(A,C,alternative='less',
  paired=TRUE,var.equal=FALSE)
result$statistic
result=t.test(A,C,alternative='less',var.equal=TRUE)
result$statistic
'''
