"""Utility and helper functions."""


def isdigit(id):
    """Checks whether input is a digit or not."""
    try:
        int(id)
        return True
    except:
        return False


def continum(alist):
    """Algorthm to to convert a numbers in a row to a spectrum.
    e.g. 1,2,3 -> 1-3
    """
    continues = [] # Continues number representation
    previous = None

    alist.sort()
    for i in alist:
        if i-1 == previous:
            last = continues[-1]
            if isinstance(last, int):
                update = [last,i]
                continues[-1] = update
            else:
                last[1] = i
                update = last
                continues[-1] = update
                continues[-1] = last
        else:
            continues.append(i)
        previous = i

    # Flatten continum:
    string = []
    for i in continues:
        if isinstance(i, list):
            string.append('%s-%s' % (i[0], i[1]))
        else:
            string.append(str(i))
    return ','.join(string)

if __name__ == '__main__':
    print continum([1,2,3,5,7,8,9])



