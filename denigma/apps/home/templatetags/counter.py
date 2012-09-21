from django import template

register = template.Library()

@register.filter
def count(value):
    """Counts the elements in a sequence."""
    return len(value)
