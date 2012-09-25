"""Provides a templatetage to replace characters dynamically."""
from django import template

register = template.Library()


@register.filter
def replace(value, pre, post):
     """Replaces any defined character."""
     return value.replace(pre, post)
