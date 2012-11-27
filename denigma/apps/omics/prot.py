"""Proteomics classes."""
from transcript import Transcript, Transcripts
from enzyme import Enzyme, Enzymes


class Proteins(Transcripts):
    pass


class Protein(Transcript):
    def __init__(self, expression=None, active=False, half_life=False, *args, **kwargs):
        Transcript.__init__(self, *args, **kwargs)        
        self.expression = expression
        self.active = active
        self.half_life = half_life

    def degradate(self):
        pass


#class Enzymes(Proteins): pass
#class Enzyme(Protein):pass


proteins = Proteins()
enzymes = Enzymes()
