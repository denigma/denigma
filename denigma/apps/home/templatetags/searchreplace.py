"""Search and replaces strings.

Usage: ::

    {{ "devok"|search:"d"|replace:"h" }}
"""
import re
from django import  template


SUBSTRING_THAT_NEVER_OCCURS = '#4x@SgXXmS'

register = template.Library

@register.filter
def search(value, search):
    return re.sub(search, SUBSTRING_THAT_NEVER_OCCURS, value)

@register.filter
def replace(value, replace):
    return re.sub(SUBSTRING_THAT_NEVER_OCCURS, value)