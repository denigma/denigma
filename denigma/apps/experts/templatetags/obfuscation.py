"""Obfuscation for Email addresses."""
from django import template

register = template.Library()


@register.filter
def obfuscate(value):
    """Replaces the at symbol of string."""
    return value.replace('@', '(at)')
