import re

from django import template
from django.utils.safestring import mark_safe

from annotations.models import GO


register = template.Library()

@register.filter
def go_links(value, term='hormone'):
    id = 'entrez_gene_id'
    rc = re.compile('\d{4,}')
    genes = dict([(str(getattr(gene, id)), gene) for gene in GO.objects.filter(go_term__icontains=term, taxid=7227)])
    def translate(match):
        if match.group(0) in genes:
            return "<a href=%s>%s</a>" % (genes[match.group(0)].get_absolute_url(), match.group(0))
        else:
            return match.group(0)
    if isinstance(value, (list, tuple, dict, set)):
        value = " ".join(map(str, value))
    return mark_safe(rc.sub(translate, value))
