import re

from django import template
from django.utils.safestring import mark_safe

from lifespan.models import Factor


register = template.Library()

@register.filter
def factor_links(value, id='entrez_gene_id'):
    if id == "entrez_gene_id":
        rc = re.compile('\d{4,}')
    else:
        rc = re.compile('\S+')
    factors = dict([(str(getattr(factor, id)), factor) for factor in Factor.objects.all()])
    def translate(match):
        if match.group(0) in factors:
            #print("lifespan.templatetag.factor_linker: Found factor %s" % match.group(0))
            return "<a href=%s>%s</a>" % (factors[match.group(0)].get_absolute_url(), match.group(0), )
        else:
            return match.group(0)
    #if isinstance(value, str): pass
    if isinstance(value, (list, tuple, dict, set)):
        value = " ".join(map(str, value))
    return mark_safe(rc.sub(translate,value))
