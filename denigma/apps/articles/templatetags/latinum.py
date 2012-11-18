from django import template

from denigma.apps.data.models import Entry

register = template.Library()

LATIN = ['in silico', 'in vitro', 'in vivo', 'in situ',
        'cis-', 'trans-', # 'omics',
        'Saccharomyces cerevisae', 'S. cerevisae',
        'Caanorhabditis elegans', 'C. elegans',
        'Drosophila melanogaster', 'D. melanogaster',
        'Mus musculus', 'M. musculus',
        'Rattus norvegicus', 'R. norvegicus',
        'Macca mullata', 'M. mullata',
        'Homo sapiens', 'H. sapiens',
        'ad libitum', 'vice versa']

@register.filter(is_safe=True)
def latin(value):
    try:
        vocabulary = Entry.objects.get(title='Latin')
    except:
        vocabulary = LATIN
    for term in vocabulary:
        value = value.replace(" %s " % term, ' *%s* ' % term)\
        .replace('(%s)' % term, '(*%s*)' % term)\
        .replace('(%s' % term, '(*%s*' % term)\
        .replace('%s)' % term, '*%s*)' % term)\
        .replace('%s.' % term, '*%s*.' % term)\
        .replace('%s,' % term, '*%s*,' % term)\
        .replace('%s-' % term, '*%s*-' % term)
    return value



