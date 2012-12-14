"""Utility functions."""


def rename_keys(d, keys):
    """Replaces the keys of a dictionary by the values of another dictionary."""
    return dict([(keys.get(k), v) for k, v in d.items()])

def intersect(*args):
    res = []
    #redundant_res = []
    for x in args[0]:                   # Scan first sequence
        for other in args[1:]:          # For all other args
            if x not in other: break    # Item in each one?
        else:
            if x not in res:            # No: break out of loop
                res.append(x)           # Yes: add items to end
                #else: redundant_res.append(x)
    return res #, redundant_res

def union(*args):
    res = []
    for seq in args:                    # for all args
        for x in seq:                   # for all nodes
            if x not in res:
                res.append(x)           # add new item to result
    return res

def count_down(n):
    """Takes a positive whole number as input and counts down that number to 0."""
    for x in reversed(xrange(n+1)):
        print x
    print("Blastoff!")

def countdown(n):
    """Prints all numbers from n to zero."""
    while n > 1:
        print n
        n += 1

def find_last(search, target):
    """Takes a search and target string and finds the last position
    of its the target string occurrence in the search string"""
    while pos != -1:
        position = search.find(target, pos+1)
        if position != -1:
            pos = position
    return pos

def print_multiplication_table(n):
    """Takes to numbers and prints out all possible multiplication between those."""
    i = 1
    while i != n+1:
        j = 1
        while j != n+1:
            print("%s * %s = %s" % (i, j, i*j))
            j += 1
        i += 1

def is_int(v):
    """Tests whether a variable can be converted into an int or not."""
    try:
        int(v)
        return True
    except:
        return False