import math

import numpy


def gammaln(x):
    if x > 0:
        return math.lgamma(x)
    else:
        return numpy.inf