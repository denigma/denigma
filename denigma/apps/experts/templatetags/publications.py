"""Provides template tags for author reference mappings."""
from django.template import Library
from django.utils.safestring import mark_safe

from Bio import Entrez
Entrez.email = 'age@liv.ac.uk'

from experts.models import Profile

register = Library()

@register.filter
def medline(author):
    """Fetches all publications of an author using the name."""
    results = {}
    name = " ".join([author.last_name, author.first_name[0]])
    r = Entrez.read(Entrez.esearch(db='pubmed', term=name))
    records = Entrez.read(Entrez.esummary(db="pubmed", id=",".join(r['IdList'])))
    for r in records:
        results[int(r['Id'])] = r['Title']
    return results

@register.filter
def authors(names):
    """Maps a list of names to experts profile if exists."""
    names = names.split('; ')
    experts = dict([(p.name_initials, p) for p in Profile.objects.all()])
    for index, name in enumerate(names):
        if name in experts:
            names[index] = '<a href="%s">%s</a>' % (experts[name].get_absolute_url(), name)
    return mark_safe("; ".join(names))
