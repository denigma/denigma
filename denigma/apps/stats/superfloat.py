"""Superfloat calculations.
http://grokbase.com/t/python/python-list/10a6ngmwaf/mantissa-and-exponent-in-base-10"""
import math

try:
    import p
except ImportError:
    p = None
try:
    from denigma.total_ordering import total_ordering
except:
    def total_ordering(func):
        return func


def sfloat(decimal):
    """Returns the mantissa and exponent in base 10."""
    return SuperFloat(decimal)

def superf(decimal):
    exp = int(math.log10(decimal))
    man = decimal/10**exp
    return man, exp
     
def frexp_10(decimal):
    """Strang manipulation conversion."""
    parts = ("%e" % decimal).split('e')
    return float(parts[0]), int(parts[1])

def frexp10(decimal):
    """mathematical conversion."""
    logdecimal = math.log10(decimal)
    return 10**(logdecimal-int(logdecimal)), int(logdecimal)

def me(n, sigfigs=4):
    s = '%%.%ig' % sigfigs % n
    if 'e' in s:
        sigfigs = len(str(n).split('e')[0]) - 2 # Determines the required significance.
        s = '%%.%ig' % sigfigs % n              # Recompute it.
        m, e = s.split('e')
    else:
        m, e = s, 0
    m, e = float(m), float(e)
    if m >= 10:
        m /= 100
        e += 2
    elif m >= 1:
        m /= 10
        e += 1
    return m, e

def logN(x, base=math.e, epsilon=1e-12):
    """logarthm function with the default base of e."""
    integer = 0
    if x < 1 and base < 1:
        raise ValueError, "logarthm cannot compute"
    while x < 1:
        integer -= 1
        x *= base
    while x >= base:
        integer += 1
        x /= base
    partial = 0.5               # 1/2
    # list = []
    x *= x                      # squaring
    decimal = 0.0
    while partial > epsilon:
        if x >= base:           # then 1_k is 1
            decimal += partial  # insert partial to the front of the list
            x = x /base         # since a_k is 1, divide the number by the base.
        partial *= 0.5
        x *= x
    return (integer + decimal)

def slogN(x, base=math.e, epsilon=1e-12):
    """logarthm function with the default base of e."""
    integer = 0
    base = sfloat(base)
    one = sfloat(1)
    if x < one and base < one:
        raise ValueError, "logarthm cannot compute"
    while x < one:
        integer -= 1
        x *= base
    while x >= base:
        integer += 1
        x /= base
    partial = 0.5               # 1/2
    # list = []
    x *= x                      # squaring
    decimal = 0.0
    while partial > epsilon:
        if x >= base:           # then 1_k is 1
            decimal += partial  # insert partial to the front of the list
            x = x / base         # since a_k is 1, divide the number by the base.
        partial *= 0.5
        x *= x
    return (integer + decimal) 

def pf(decimal, precision=2):
    """Converts a float into a pretty form."""
    if decimal == 0: return 0
    string = str(decimal)
    if string == '0': return 0
    #if decimal <= 0.001:
    if 'e' in string:
        base, exponent = string.split('e')
        base = str(round(float(base), precision))
        pretty = float(base+'e'+exponent )
    elif decimal < float('0.'+'0'*precision+'1'):
        string = "".join(string.split('.')[1])
        zeros = 0
        while string.startswith('0'):
            string = string[1:]
            zeros += 1
        try:
            string = float(string[:precision+1])/10**precision
        except: print string, zeros
        pretty = "{0}e-{1}".format(string, zeros)
    else:
        pretty = round(decimal, 3)

    return pretty


@total_ordering
class SuperFloat(object):
    """A super precise decimal numbers."""
    def __init__(self, decimal, exponent=None):
        if not exponent:
            self.man = me(decimal)[0]
            self.exp = int(me(decimal)[1])                 # mantissa           # exponent
        else:
            self.man, self.exp = decimal, exponent
        
    def __str__(self):
        return "{0}e{1}".format(self.man*10, int(self.exp-1))

    def __sub__(self, other):
        selfN = self.man * int('1'+'0' * abs(self.exp))
        print selfN, (self.man, self.exp)
        otherN = other.man * int('1'+'0' * abs(other.exp))
        print otherN, (other.man, other.exp)
        subtract = abs(otherN - selfN) #/ (int('1'+'0' *  abs(max(self.exp, other.exp))))
        print subtract
        return SuperFloat(subtract, max(self.exp, other.exp))

    def __mul__(self, other):
        return SuperFloat(self.man * other.man, self.exp + other.exp)

    def __div__(self, other):
        return SuperFloat(self.man / other.man, self.exp - other.exp)

    def __eq__(self, other):
        return self.exp == other.exp and self.man == other.man

    def __lt__(self, other):
        """Method triggered by <"""
        return (self.exp, self.man) < (other.exp, other.man)

def testLogN():
    value = 4.5
    print("x = {0}".format(value))
    print("ln(x) = {0}".format(logN(value)))
    print("log4(x) = {0}".format(logN(value, base=4)))

if __name__ == '__main__':
    d1 = 1.3181918357e-69
    d2 = 1.29918690857e-174
    
    sf1 = sfloat(d1)
    sf2 = sfloat(d2)
    print sf1, sf2
    print sf1 < sf2, sf1 > sf2, sf1 <= sf2, sf2 >= sf1
    print slogN(sf1), logN(d1), math.log(d1)
    print slogN(sf2),logN(d2), math.log(d2)
    print "Subtraction: "
    print sf1-sf2, d1-d2

    print

    string1 = frexp_10(d1)
    string2 = frexp_10(d2)
    print string1, string2
    
    s1 = frexp10(d1)
    s2 = frexp10(d2)
    print s1, s2

    me1 = me(d1, 11)
    me2 = me(d2, 12)
    print me1, me2
    testLogN()
    print me1 < me2, me1 > me2, me1 <= me2, me1 >= me2

