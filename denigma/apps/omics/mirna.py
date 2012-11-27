"""microRNAs"""


class miRNAs(dict):
    def __init__(self):pass


class miRNA:
    def __init__(self, chr, start, stop, strand, acc, id, species=None, description=None, comment=None, sequence=None):
        self.chr = chr
        self.start = int(start)
        self.stop = int(stop)
        if strand == "+": self.strand = 1
        else: self.strand = -1
        self.sequence = sequence

        self.species = species

        self.acc = acc
        self.id = id
        self.description = description
        self.comment = comment
        
        self.mature = {}
    
        mirnas[id] = self

    def __repr__(self):
        attributes = (self.id, self.acc, self.chr, self.start, self.stop, self.strand, self.mature, self.description, self.comment)
        string = '%s\t'*len(attributes)
        string = string[:-1]
        return string % attributes

    def __str__(self):
        L = []
        for k, v in vars(self).items():
            if isinstance(v, dict):
                for i in v:
		    L.append('')
		    attribute = eval('vars(self.'+k+'["'+i+'"]).items()')
                    for attr, value in attribute: #vars(self.k[i]).items():
                        L.append('%s = %s' % (attr, value))
                L.append('')
            else:
                L.append('%s = %s' % (k, v)) 
        return '\n'.join(L)

    def __cmp__(self, other):
        """Tests whether a sequence is within the gene region."""
        if other.stop - other.start == 1: other.start = self.stop    # Should be other.stop instead of other.start in the case of an SNP. ALternitively test: isinstance(other, SNP)
        return other.start >= self.start and other.stop <= self.stop    


class miRNAmature():
    """A matures miRNA."""
    def __init__(self, acc, id, chr, start, stop, strand, sequence):
        self.acc = acc
        self.id = id
        self.chr = chr
        self.start = start
        self.stop = stop
        self.strand = strand
        self.sequence = sequence

        #self.seed {}

    def __repr__(self):
        #string = '%s\t'*len(vars(self).keys())
        #string = string[:-1]
        return ' '.join(map(str, vars(self).values()))

    def __str__(self):
        L = []
        for k, v in vars(self).items():
            if isinstance(v, dict):
                for i in v:
		    L.append('')
		    attribute = eval('vars(self.'+k+'["'+i+'"]).items()')
                    for attr, value in attribute: #vars(self.k[i]).items():
                        L.append('%s = %s' % (attr, value))
                L.append('')
            else:
                L.append('%s = %s' % (k, v)) 
        return '\n'.join(L)


mirnas = miRNAs()
