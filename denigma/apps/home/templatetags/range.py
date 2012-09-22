from django.template import Library


register = Library()

@register.filter
def get_range(value):
    """Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results wiht the HTML:
    <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li<2. Do something</li>

        Instead of 3 one may use the variable set in te views.
    """
    return range(value)

@register.filter
def get_range_plus_one(value):
    """Filter - returns a list containing values from 1 to value"""
    return range(1, value+1)