"""Provides a function to remove whitespaces"""
from django import template

register = template.Library()


@register.filter
def despace(value):
    """Removes whitespace characters from a string."""
    return value.replace(' ', '')

