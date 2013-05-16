# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.safestring import mark_safe

#try:
from lifespan.models import Factor
#except: Factor = None

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
            return "<a href=%s>%s</a>" % (factors[match.group(0)].get_absolute_url(), factors[match.group(0)].symbol, )
        else:
            return match.group(0)
    #if isinstance(value, str): pass
    if isinstance(value, (list, tuple, dict, set)):
        value = " ".join(map(str, value))
    return mark_safe(rc.sub(translate, value))

@register.filter
def symbols(value):
    rc = re.compile('[*\w\d-]{3,}|\w+')
    links = ['\n']

    factors = dict([(factor.symbol, factor.symbol) for factor in Factor.objects.all()])
    factors['TakeOut'] = u'to'
    factors['Shaker'] = u'Sh'
    del factors['to']
    del factors['g']
    del factors['Arntl']

    def translate(match):
        factor = match.group(0)
        factor_name = factor.replace('*', '')
        if factor_name in factors and not factor.startswith('_') and not factor_name.endswith('_'):
            target = '.. _%s: http://denigma.de/lifespan/factor/%s' % (factor_name, factors[factor_name])
            if target not in value and target not in links:
                links.append(target)
            return factor_name + '_'
        else:
            return factor
    result = rc.sub(translate, value)
    result += "\n".join(links)
    #print result

    return mark_safe(result)

if __name__ == '__main__':
    rc = re.compile('[\w\d-]{3,}|\w+') #[a-zA-Z0-9]
    string = 'Sh_ some more text Hsp23 df Trx-2 dfs'
    print re.findall(rc, string)
