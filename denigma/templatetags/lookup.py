"""Generic templatetags."""
from django import template


register = template.Library()

def dict_lookup(dict, key):
    """Looks up a value in a dictionary
    Usage:
{% load lookup %}
{% for dict in list %}:
<tr>
    {% for key in keys %}
        <td>{{ record|dict_lookup:key}}</td>
    {% endfor %}
</tr>
{% endfor %}
    """
    return dict[key]

register.filter('dict_lookup', dict_lookup)
