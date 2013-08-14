import re


class Index(dict):
    @staticmethod
    def create(documents):
        for document in documents:
            for word in document:
                index = Index.lookup(word)
                if index < 0:
                    position = Index.add(word)
                    Index.append((position, document.id))
                else:
                    Index.append(index, document.id)
    @staticmethod
    def loopkup(word):
        if word in Index:
            return Index[word]
        return None

    @staticmethod
    def add(word):
        Index[word] = word

    @staticmethod
    def append(index, id):
        pass


def multiwordReplace(text, wordDic):
   """Takes a text and replaces words that match a key in a dictionary with the
   associated value, return the changed text."""
   rc = re.compile('|'.join(map(re.escape, wordDic)))
   def translate(match):
       return wordDic[match.group(0)]
   return rc.sub(translate, text)

def multiReplace(text, wordDic):
    """Takes a text and replaces words that match the key in a dictionary with
    the associated value, return the changed text."""
    for key in wordDic:
        text = text.replace(key, wordDic[key])
    return text


wordDic = {
'mega': 'hyper',
'nice': 'awesome'
}

def test():
   from timeit import Timer
   NTIMES = 100000
   testlist = [multiwordReplace, multiReplace]
   for func in testlist:
       print "{n}(): {u:.2f} usecs".format(n=func.__name__, u=Timer(
             "{n}(text, wordDic)".format(n=func.__name__),
             "from __main__ import {f}, text, wordDic".format(
                    f=",".join(x.__name__ for x in testlist))
             ).timeit(number=NTIMES) * 1.e6/NTIMES)

def union(a,b):
    """A procedure that takes as input two lists and returns the set."""
    for e in b:
        if e not in a:
            a.append(e)


def product_list(alist):
    """Takes as input a list of numbers, and returns the product.

    It returns a number that is the result of multiplying all those numbers together.
    """
    if alist:
        product = alist[0]
        for i in alist[1:]:
            product *= i
        return product
    else:
        return 1


def greatest(alist):
    """Takes as input a list of positive numbers,
    and returns the greatest number in that list.

    If the input list is empty, the output should be 0."""
    if alist:
        return max(alist)
    else:
        return 0

def check_sudoku(instance):
    numbers = range(10)
    print(len(instance))
    print([(number, []) for number in xrange(len(instance))])
    print(zip([(number, []) for number in xrange(len(instance))]))
    columns = dict([(number, []) for number in xrange(len(instance))])
    for index, row in enumerate(instance):
        row_numbers = []
        for number in row:
            if number not in numbers or number in row_numbers or number > len(instance) or not number:
                return False
            row_numbers.append(number)
        for index, column in enumerate(row):
            if column in columns[index] or column > len(instance) or not column: return False
            columns[index].append(column)
    return True

def symmetric(matrix):
    """Checks whether a matrix is symmetric.
    A list is symmetric if the first row is the same as the first column,
    the second row is the same as the second column and so on.
    This procedure takes as a list as input, and returns the boolean True
    if the list is symmetric and False if it is not."""
    inverse_matrix = []

    for x in zip(*matrix):
        inverse_row = []
        for y in x:
            inverse_row.append(y)
        inverse_matrix.append(inverse_row)
    if len(matrix) != len(inverse_matrix):
        return False
    for row in xrange(len(matrix)):
        for i, x in enumerate(matrix[row]):
            if x != inverse_matrix[row][i]:
                return False
    return True


def list_mean(numbers):
    """Takes a list of numbers as its input and returns
    the mean of the numbers in the list."""
    return 1.*sum(numbers)/len(numbers)


if __name__ == '__main__':
   text = "This are mega algorithms which make life nice."
   print multiwordReplace(text, wordDic)
   print multiReplace(text, wordDic)
   test()

