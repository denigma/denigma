"""HUGO Gene Nomenclature Committee (HGNC)
#symbol withdrawn, see in name"""
import os

from files import File, HTML
from omics import genes


def main():
    os.chdir(path)
    html = HTML(url="http://www.genenames.org/cgi-bin/hgnc_downloads.cgi") # Check html for attributes.

    attributes = html.find_between("</td> <td>", "</td>", '"', all=True) # Retrieve all aviable attributes.

    print("Number of attributes: %s" % len(attributes)) # Check number of attributes.

    # Building url:
    url_begin = "http://www.genenames.org/cgi-bin/hgnc_downloads.cgi?title=Core+Data"
    url_context = ";col="+";col=".join(attributes) #col=gd_hgnc_id;col=gd_app_sym;col=gd_app_name;col=gd_status;col=gd_prev_sym;col=gd_aliases;col=gd_pub_chrom_map;col=gd_pub_acc_ids;col=gd_pub_refseq_ids;
    url_end = ";status=Approved;status=Approved+Non-Human;status=Entry+Withdrawn;status_opt=3;=on;where=;order_by=gd_app_sym_sort;limit=;format=text;submit=submit;.cgifields=;.cgifields=status;.cgifields=chr"
    url = url_begin + url_context + url_end

    f = File(name="hgnc.txt", url=url, path=path)
    contents = f.parse(printing=False, header=True)
    genes.name = "HGNC"
    genes.key = "hgnc"
    genes.taxid = 9606
    genes.addData(contents)
    genes.save()
    genes.buildMappings()
    
if __name__ == '__main__': path = '.'; main()
else: path = os.path.join(os.path.split(__file__)[:-1])[0]

"""
HGNC ID
Approved Name
Locus Type
Previous Symbols
Synonyms
Chromosome
Date Modified
Date Name Changed
Enzyme IDs
Ensembl Gene ID
Specialist Database Links
Pubmed IDs
Gene Family Tag
Record Type
Secondary IDs
VEGA IDs
GDB ID (mapped data)
OMIM ID (mapped data supplied by NCBI)
UniProt ID (mapped data supplied by UniProt)
UCSC ID (mapped data supplied by UCSC)
Rat Genome Database ID (mapped data supplied by RGD)
Approved Symbol --> symbols
Status
Locus Group
Previous Names
Name Synonyms
Date Approved
Date Symbol Changed
Accession Numbers
Entrez Gene ID
Mouse Genome Database ID
Specialist Database IDs
RefSeq IDs
Gene family description
Primary IDs
CCDS IDs
Locus Specific Databases
Entrez Gene ID (mapped data supplied by NCBI)
RefSeq (mapped data supplied by NCBI)
Ensembl ID (mapped data supplied by Ensembl)
Mouse Genome Database ID (mapped data supplied by MGI)
"""
