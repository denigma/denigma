from django.template import Library

from Bio import Entrez
Entrez.email = 'age@liv.ac.uk'


register = Library()

@register.filter
def medline(author):
    results = {}
    name = "-".join([author.last_name, author.first_name[0]])
    r = Entrez.read(Entrez.esearch(db='pubmed', term=name))
    records = Entrez.read(Entrez.esummary(db="pubmed", id=",".join(r['IdList'])))
    for r in records:
        results[r['Id']] = r['Title']
    return results