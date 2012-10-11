"""Enables to load dynamically data entries in templates."""
from django import template

from data import get


register = template.Library()

@register.filter
def entry(value):
    return get(value)