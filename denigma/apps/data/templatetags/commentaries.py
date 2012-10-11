from django import template

from denigma.apps.data.models import Entry, Relation


register = template.Library()

@register.inclusion_tag('data/commentaries.html')
def display_commentaries(entry_pk):
    entry = Entry.objects.get(pk=entry_pk)
    commentaries = Relation.objects.filter(be__title='comments on',to=entry)
    return {'commentaries': commentaries}
