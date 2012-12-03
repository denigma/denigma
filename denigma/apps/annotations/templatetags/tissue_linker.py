import re

from django import template
from django.utils.safestring import mark_safe

#try:
from annotations.models import Tissue
#except:pass


register = template.Library()

@register.filter
def tissue_links(value):
    links = ['\n']
    #try:
    tissues = dict([(str(getattr(tissue, 'name')), tissue) for tissue in Tissue.objects.all()])
    #except: tissues = {'heart': 'heart'}
    def translate(match):
        tissue_name = match.group('tissue')
        tissue = tissue_name.replace('`' , '')
        if tissue in tissues and not tissue_name.startswith('`') and not tissue_name.endswith('`'): # and not tissue.startswith('_') and not tissue.endswith('_')
            if ' ' in tissue:
                 tissue_name = tissue.replace(' ', '-')
                 #print tissue_name
                 tissue = "`%s`" % tissue
            else:
                tissue_name = tissue
            target = '.. _%s: http://denigma.de/annotations/tissue/%s' % (tissue, tissue_name)
            if target not in value and target not in links:
                links.append(target)
            return tissue + '_'
        else:
            return tissue_name

    rc = re.compile('(?P<tissue>\w{3,}( \w{3,})?)')
    value = rc.sub(translate, value)
    #rc = re.compile(r'(?P<tissue>\b([a-z`]+)\b)') #|\b([a-z]+)\b \b([a-z]+)\b) #r'.?(?!`)(\b([a-z]+)\b).?(?!`)'
    #value = rc.sub(translate, value)
    value += "\n\n"+"\n".join(links) +'\n\n'
    return mark_safe(value)

if __name__ == '__main__':
    string = "In the heart DR up-regulates transcripts are associated to insect cuticle protein, signal peptide, Cytoplasmic, Helix-loop-helix-motif and folate biosynthesis, while it down-regulates glycosidase and innate immunity related terms (Table 7)."
    print tissue_links(string)