from django import template

register = template.Library()

@register.filter
def unicode(obj):
    return obj.__unicode__()