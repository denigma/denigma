"""Probalistic datastructure through Hashing.
Inspired by:
https://github.com/ctb/khmer-ngram/blob/master/hash.py
http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-handling-ridiculous-amounts-of-data-with-probabilistic-data-structures-4899047

TODO:
 - check out the book example whether they are of any use.
"""

MAX_K = 16
DEFAULT_K = 8


def is_prime(n):
    """Checks if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    for x in xrange(2, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def get_n_primes_above_x(n, x):
    """Steps forward unitil n primes (other than 2) have been found
    that are smaller than x."""
    primes = []
    i = x+1
    if i % 2 == 0:
        i += 1
    while len(primes) != n and i > 0:
        if is_prime(i):
            primes.append(i)
        i += 2
    return primes

def hash(word):
    """Hash function.
    Defines a has function (word => num)"""
    assert len(word) <= MAX_K
    value = 0
    for n,ch in enumerate(word):
        value += ord(ch) * 128**n
    return value


class BloomFilter(object):
    """ Creates a number of hash tables."""
    allchars = "".join([ chr(i) for i in xrange(128) ])
    
    def __init__(self, tablesizes, k=DEFAULT_K):
        self.tables = [(size, [0] * size) for size in tablesizes ]
        self.k = k

    def add(self, word):
        """Insert; ignore collisions."""
        val = hash(word)
        for size, ht in self.tables:
            ht[val % size] = 1

    def __contains__(self, word):
        val = hash(word)
        return all( ht[val % size] \
                    for (size, ht) in self.tables )

    def insert_text(self, text):
        """Storing text in a Bloom filter."""
        for i in range(len(text)-self.k+1):
            self.add(text[i:i+self.k])

    def occupancy(self):
        return [ sum(t)/float(len(t)) for _, t in self.tables ]

def first_next_word(bf, word):
    prefix = word[1:]
    for ch in bf.allchars:
        word = prefix + ch
        if word in bf:
            return ch, word
    return None, None


def retrieve_first_sentence(bf, start):
    word = start[-bf.k:]
    while 1:
        ch, word = first_next_word(bf, word)
        if ch is None:
            break
        start += ch
    return start

def next_words(bf, word):
    """Try all 1-ch extensions."""
    prefix = word[1:]
    for ch in bf.allchars:
        word = prefix + ch
        if word in bf:
            yield ch

def retrieve_all_sentences(bf, start):
    word = start[-bf.k:]
    n = -1
    for n, ch in enumerate(next_words(bf, word)):
        ss = retrive_all_sentences(bf, start + ch)
        for sentence in ss:
            yield sentence
    if n < 0:
        yield start

def count_connected_graph(bf, word, cutoff=10, keepter=None):
    assert len(word) == bf.k
    if keeper is None:
        keeper = set()
    if word in keeper:
        return len(keeper)

    keeper.add(word)
    if len(keeper) >= cutoff:
        return len(keeper)

    for n, ch in enumerate(next_words(bf, word)):
        count_connected_graph(bf, word[1:] + ch, cutoff=cutoff, keeper=keeper)

    for n, ch in enumerate(previuos_words(bf, word)):
        count_connected_graph(bf, ch + word[:-1], cutoff=cutoff, keeper=keeper)

    return len(keeper)
    
if __name__ == '__main__':
    x = BloomFilter([1001, 1003, 1005])
    print 'oogaboog' in x
    x.add('oogaboog')
    print 'oogaboog' in x

    x = BloomFilter([2]) # ... false positives
    x.add('a')
    print 'a' in x
    print 'b' in x
    print 'c' in x

    # Storing and retrieving text
    x = BloomFilter([1001, 1003, 1005, 1007])
    x.insert_text('foo bar bazibif zap!')
    x.insert_text('the quick brown fox jumped over the lazy dog')
    print retrieve_first_sentence(x, 'foo bar ')
    print retrieve_first_sentence(x, 'the quic')
    print retrieve_first_sentence(x, 'bazibif zap!')

    # Sequence assembly (Bruin graph approach):
    x = BloomFilter([1001, 1003, 1005, 1007])
    x.insert_text('the quick brown fox jumped ')
    x.insert_text('jumped over the lazy dog')
    print retrieve_first_sentence(x, 'the quic')

    # Repeptitive strings are the devil
    x = BloomFilter([1001, 1003, 1005, 1007])
    x.insert_text('nanana, batman!')
    x.insert_text('my chemical romance: nanana')
    print retrieve_first_sentence(x, "my chemical")

    # Retrieval errors:
    x = BloomFilter([1001, 1003]) ## small Bloom filter...
    x.insert_text('the quick brown fox jumped over the lazy dog')
    print retrieve_first_sentence(x, 'the quic')

#234567891123456789212345678931234567894123456789512345678961234567897123456789
    
    
