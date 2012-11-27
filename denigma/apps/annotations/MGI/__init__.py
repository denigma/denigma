"""Mouse Genome Information Retrieval."""
import os
from files import FTP, File, Folder
from omics import genes
from utils import rename_keys


def change_keys(d): 
    """A helper function to remove numbers from key strings of a dict.
    Inspired by:
    http://stackoverflow.com/questions/2213334/in-python-i-have-a-dictionary-how-do-i-change-the-keys-of-this-dictionary"""
    if type(d) is dict:
        return dict([(k.split('. ')[1], change_keys(v)) for k, v in d.items()])
    else:
        return d

def main(interactions=False, download=True, parse=True, withdrawn=True,
         cleanup=True):
    """Performs the download of interaction and annotation files from MGI.
    Builds a gene annotation file and mapping tables.
    TODO:
    - Inspect and eventually use interaction file, else discard from this module.
    - Also check whether other information from MGI is worse to integrate
      such as homology or phenotypes."""
    os.chdir(path)
    genes.name = 'MGI'
    genes.key = 'mgi'
    folder = Folder(path)
    
    if interactions:
        ftp = FTP(url='ftp://ftp.informatics.jax.org/pub/protein-interaction-data/',
                  path=path)
        ftp.download(path)
        
    if download:
        url = "ftp://ftp.informatics.jax.org/pub/reports/"
        files = ["MRK_List1.rpt", "MRK_List2.rpt",
                 "MGI_Coordinate.rpt", "MRK_Sequence.rpt",
                 "MRK_SwissProt_TrEMBL.rpt", "MRK_VEGA.rpt",
                 "MRK_ENSEMBL.rpt", "MGI_EntrezGene.rpt"]
        # MPheno_OBO.ontology, VOC_MammalianPhenotype.rpt, MGI_PhenotypicAllele.rpt, HMD_HumanPhenotype.rpt
        for f in files:
            f = File(url=url+f) # automatically does f.download()
            res = f.parse(header=True,printing=False)
            folder.downloads.append(f.name)
            
    if parse:
        folder.update()
        if withdrawn: filename = "MRK_List1.rpt"
        else: filename = "MRK_List2.rpt"
        data = folder[filename].parse(header=True,printing=False)
        genes.addData(data, key='mgi', taxid=10090)

        data = folder["MGI_Coordinate.rpt"].parse(header=True,printing=False)
        for i in data:
            i = change_keys(i)
            i['taxid'] = 10090
            genes.add(i)

        data = folder['MRK_Sequence.rpt'].parse(header=True, printing=False)
        genes.addData(data, key='mgi', taxid=10090)

        header = "mgi symbol status name cm_position chromosome	type "\
        "secondary_accession_ids id synonyms feature_types start "\
        "stop strand biotypes".split()
        data = folder["MGI_EntrezGene.rpt"].parse(header=header,printing=False)
        genes.addData(data, key="mgi", taxid=10090)
        print len(genes)

    if cleanup:
        if interactions: ftp.remove(confirm=False)
        for f in folder.downloads:
            folder.remove(f)

    genes.keep("category", "Gene")
    genes.remove("name", "withdrawn")
    genes.save()
    genes.buildMappings()

if __name__ == '__main__':
    path = '.';
    main(interactions=True, download=True, parse=True, withdrawn=False)
else:
    path = os.path.join(os.path.split(__file__)[:-1])[0]
    
#234567891123456789212345678931234567894123456789512345678961234567897123456789

#MGI_Coordinate.rpt: representative genome start/stop and NCBI genome start/stop differ sometimes.
"""
mgi
symbol
name
chromosome
start
stop
strand
id
ensemble_gene
vega
unists
mirbase
"""

"""
1. MGI accession id
2. marker type
3. marker symbol
4. marker name
5. representative genome id
6. representative genome chromosome
7. representative genome start
8. representative genome end
9. representative genome strand
10. representative genome build
11. Entrez gene id
12. NCBI gene chromosome
13. NCBI gene start
14. NCBI gene end
15. NCBI gene strand
16. Ensembl gene id
17. Ensembl gene chromosome
18. Ensembl gene start
19. Ensembl gene end
20. Ensembl gene strand
21. VEGA gene id
22. VEGA gene chromosome
23. VEGA gene start
24. VEGA gene end
25. VEGA gene strand
26. UniSTS gene chromosome
27. UniSTS gene start
28. UniSTS gene end
29. MGI QTL gene chromosome
30. MGI QTL gene start
31. MGI QTL gene end
32. miRBase gene id
33. miRBase gene chromosome
34. miRBase gene start
35. miRBase gene en
36. miRBase gene strand
37. Roopenian STS gene start
38. Roopenian STS gene end
"""
