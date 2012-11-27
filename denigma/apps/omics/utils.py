"""Omics utility functions."""


numeral_map = zip( (1000, 900, 500, 100, 90, 50, 40, 10, 9, 5, 4, 1), ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'V' 'IV', 'I') )

def int_to_roman(i):
    try:
        i = int(i)
        result = []
        for integer, numeral in numeral_map:
            count = int(i/integer)
            result.append(numeral*count)
            i -= integer*count
        return ''.join(result)
    except:
        return i

def roman_to_int(n):
    n = unicode(n).upper()
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result

def evalu(string):
    '''Converts a string to float, number if possible'''
    try:
        if "." in string or "e" in string or "E" in string: return float(string)   # Try to convert to float
        else: raise Exception
    except:
        try: return int(string)     # Try to convert to int
        except: return string 
    
#taxids = [4932, 5145, 6239, 7227, 9606, 10036, 10090, 10116, 559292] # '4896',     

def t(name):
    """A helper function which combines entrez and wormbase."""
    gene = entrez.find(name)
    print gene, '\n', wormbase[gene.wormbase]
