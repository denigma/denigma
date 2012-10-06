"""Its the final countdown!"""


class Counter:
    """Keeps track of progression in looping through a sequence."""
    def __init__(self, sequence, msg=None):
        """Start the counter."""
        self.length = len(sequence)
        self.n = 0          # count
        self.pb = 0         # percentage before
        if msg:
            print '\n', msg,# message
        
    def count(self):
        """Continue counter."""
        self.n += 1
        self.pa = 100*self.n/self.length # percentage after
        if self.pb != self.pa:
            print self.pb
            self.pb = self.pa

def count(instance):
    """Adds a counter to a sequence."""
    Super = instance.__class__
    class CountIt(Super, Counter):
        def __init__(self, *args, **kwargs):
            #super(CountIt, self).__init__()
            Super.__init__(self, *args, **kwargs)
            Counter.__init__(self, sequence=instance)
        def next(self):
            Super.__init__(self)
            self.count()
    count = CountIt()
    count.__dict__.update(instance.__dict__)
    return count

    
if __name__ == '__main__':
    sequence = range(1,100000000)
    counter = Counter(sequence)
    for i in sequence:
        counter.count()
##    seq = count(sequence)
##    for i in seq:
##        pass
    
