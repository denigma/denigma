"""Flexible template tags for linking to NCBI resources."""
import re

from django.utils.safestring import mark_safe


BASE_URL = 'http://www.ncbi.nlm.nih.gov/'

def geneid(value):
    """Converts a NCBI/Entrez gene id into a link to NCBI gene record."""
    return mark_safe('<a href="%s/genes/%s">%s</a>' % (BASE_URL, value, value))

def pubmeds(value):
    """Transforms PubMed IDs into links to the respective PubMed record."""
    rc = re.compile('(?P<id>[1-9]\d{6,})')
    def translate(match):
        return "<a %spubmed/%s>%s</a>" %\
               (BASE_URL, match.group('id'), match.group('id'))
    return mark_safe(rc.sub(translate, value))