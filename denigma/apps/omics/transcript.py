"""Transcriptomics classes."""
from gen import Gene, Genes


class Transcripts(Genes):
    pass


class Transcript(Gene):
    def __init__(self, gene=None, *args, **kwargs):
        Gene.__init__(self, *args, **kwargs)
        self.gene = gene


transcripts = Transcripts()
