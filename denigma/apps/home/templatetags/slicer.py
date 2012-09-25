"""Slices sequence like objects"""
from django import template

register = template.Library()

@register.filter
def slice(value, index):
    """Slices a string at index."""
    return value[:int(index)]
