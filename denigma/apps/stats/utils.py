"""Utlilities for perfoming statistics.
Contians so far only unbiased variation and standard variation function"""
from __future__ import division
import numpy as np

def unbiased_var(X):
    n = len(X)
    sample_SS = sum(X**2) - sum(X)**2 / n
    return sample_SS/ (n-1)
    
def unbiased_std(X):
    return np.sqrt(unbiased_var(X))

