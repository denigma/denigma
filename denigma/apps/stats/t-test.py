"""Performs t-tests. Contains a one-sampled t-test function.
This module should be merged with ttest.py"""
from __future__ import division
import numpy as np
#from transcendental import stdtr
from scipy.special import stdtr

from utils import unbiased_std

def one_sample_t(A,mu):
    n = len(A)
    df = n - 1
    z = np.mean(A) - mu 
    z /= unbiased_std(A)
    t = z * np.sqrt(n)
    return t, stdtr(df,t)


def test(A,mu):
    result = one_sample_t(A,mu)
    print 't-statistic  p-value'
    print '%5.3f         %5.3f' % result
    
if __name__ == '__main__':
    A = np.array([3.1,2.3,2.1,1.7])
    B = np.array([2.1,1.8,2.7,2.4])
    test(A,mu=3)
    test(B,mu=3.5)
'''
R code:
A = c(3.1,2.3,2.1,1.7)
t.test(A, alternative='less',mu=3)
B = c(2.1,1.8,2.7,2.4)
t.test(B, alternative='less',mu=3.5)
'''
##a =[123,123,134,123]#
##b = [1121126, 1211231232, 11241334, 113412334]
##d = [5,5,5,5]

