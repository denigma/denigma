"""Statistics module to calculate effect size."""
import math


def m(values):
    """Calculates the mean of the values."""
    size = len(values)
    sum = 0.0
    for n in xrange(0, size):
        sum += values[n]
    return sum/size

def sd(values, mean):
    """Calculates standard deviation."""
    size = len(values)
    sum = 0.0
    for n in xrange(0, size):
        sum += math.sqrt((values[n] - mean)**2)
    return math.sqrt((1.0/(size-1))*(sum/size))

def sD(values, mean=None):
    """Formula for std dev approximation based on a sample set on Wikipedia."""
    if not mean:
        mean = m(values)
    size = len(values)
    sum = 0.0
    for n in xrange(0, size):
        sum += ((values[n] - mean)**2)
    return math.sqrt(1.0/(size-1))*sum

def sd_pooled(exp, ctr):
    return math.sqrt((len(exp)-1)*sD(exp)**2 + (len(ctr)-1)*sD(ctr)**2)\
                                /(len(exp)+len(ctr)-2)

def effect_size(exp, ctr):
    """Effect size is the standardised mean difference between 2 experimental groups."""
    #if len(exp) == 1 or len(ctr) == 1: return None
    #else:
    return ( sum(exp)/len(exp) - sum(ctr)/len(ctr) ) / sd_pooled(exp, ctr)

def main():
    exp = [1,2,3]
    ctr = [4,5,6]
    es = effect_size(exp, ctr)
    print es

if __name__ == '__main__':
    main()

#2345678911234567892123456789312345678941234567895123456789512345678961234567897123456789
