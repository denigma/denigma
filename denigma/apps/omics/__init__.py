"""Biological entities."""
from gen import Gene, Genes, genes
from transcript import Transcript, Transcripts, transcripts #  Rename to trans
from prot import Protein, Proteins, proteins, Enzyme, Enzymes, enzymes
from go import GOs, GO, gos
from inter import Interactions, interactions, Interaction
from signature import Signature, Signatures # Rename to sign


def main():
    dbs = 'SGD', 'Entrez', 'Ensembl', 'UniProt', 'SGD', 'WormBase', 'FlyBase', 'MGI', 'HGNC'
    for db in dbs:
        genes = Genes(db)
        genes.buildMappings()


if __name__ == '__main__':
    main()
