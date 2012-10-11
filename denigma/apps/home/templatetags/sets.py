from django import template


register = template.Library()

@register.filter
def unique(value):
    return set(value)