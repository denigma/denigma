"""Provides a templatetage to replace characters dynamically."""
from django import template

register = template.Library()


@register.filter
def replace(value, args=None):
    """Replaces any defined string by another string. Separate strings by ' | '
    By default return is replaces by html break."""
    if not args:
        pre, post = '\r', '<br>'
    else:
        pre, post = args.split(' | ')
    return value.replace(pre, post)
