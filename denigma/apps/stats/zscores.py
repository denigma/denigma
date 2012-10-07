"""Converts a p-value to a z-score.
Depreciated! This function was incorporated into combp,
as it was only requered there so far."""
import numpy as np
import scipy.stats

TINY = 1e-15

def zscore(pvalue):
    """Return the z-score corresponding to a given p-value."""
    pvalue = np.minimum(np.maximum(pvalue, TINY), 1.-TINY)
    z = scipy.stats.norm.isf(pvalue)
    return z

if __name__ == '__main__':
    print(zscore(0.05))
