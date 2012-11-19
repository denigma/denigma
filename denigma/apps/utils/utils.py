import re


class Index(dict):
    @staticmethod
    def create(documents):
        for document in documents:
            for word in document:
                index = Index.lookup(word):
                if index < 0:
                    position = self.add(word)
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
        self[word] =

    @staticmethod
    def append(index, id):


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





if __name__ == '__main__':
   text = "This are mega algorithms which make life nice."
   print multiwordReplace(text, wordDic)
   print multiReplace(text, wordDic)
   test()

