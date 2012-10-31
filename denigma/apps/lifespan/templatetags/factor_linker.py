import re

from django import template
from django.utils.safestring import mark_safe

#try:
from lifespan.models import Factor
#dexcept: Factor = None


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
    return mark_safe(rc.sub(translate, value))

@register.filter
def symbols(value):
    rc = re.compile('\w{2,}')
    links = ['\n']
    factors = dict([(str(factor.symbol), factor) for factor in Factor.objects.all()])
    del factors['to']

    def translate(match):
        factor = match.group(0)
        if factor in factors and not factor.startswith('_') and not factor.endswith('_'):
            target = '.. _%s: http://denigma.de/lifespan/factor/%s' % (factor, factor)
            if target not in value and target not in links:
                links.append(target)
            return factor + '_'
        else:
            return factor
    result = rc.sub(translate, value)
    result += "\n".join(links)
    print result

    return mark_safe(result)

if __name__ == '__main__':
    rc = re.compile('\w{2,}') #[a-zA-Z0-9]
    string = 'Sh_ some more text Hsp23 df '
    print re.findall(rc, string)
