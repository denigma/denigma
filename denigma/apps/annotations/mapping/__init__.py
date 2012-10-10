from annotations.models import gene2ensembl, EnsemblEntrezGeneId


def map(ids):
    # 1. Identify whether it recieves a single gene id/symbol/name or multiple
    if isinstance(ids, (list, tuple, dict)):
        pass
    else:
        ids = [ids]
    for id in ids:
        gene_id = None
        try:
            if id.startswith('FBgn'):
                # Ensembl gene
                gene_id = gene2ensembl.objects.get(ensembl_gene_id=id).entrez_gene_id
            elif id.startswith('FBtr'):
                # Ensembl transcript
                gene_id = gene2ensembl.objects.get(ensembl_rna_id=id).entrez_gene_id
            #print id, gene_id
        except (gene2ensembl.DoesNotExist)  as e: #or EnsemblEntrezGeneId.DoesNotExist)
            #print id, e
            pass
        except gene2ensembl.MultipleObjectsReturned as e:
            try:
                gene_ids = EnsemblEntrezGeneId.objects.filter(ensembl_gene_id=id)
                gene_id = gene_ids[0].entrez_gene_id
                #print id, gene_ids, e
            except IndexError:
                pass
    return gene_id

