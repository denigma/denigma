from django import template
from django.db.models import Q

from denigma.apps.data.models import Entry, Relation


register = template.Library()

@register.inclusion_tag('data/relations.html')
def display_relations(entry_pk):
    entry = Entry.objects.get(pk=entry_pk)
    relations = Relation.objects.filter(Q(fr=entry) | 
                                         Q(be=entry) | 
                                         Q(to=entry))
    return {'relations': relations}
#234567891123456789212345678931234567894123456789512345678961234567897123456789
