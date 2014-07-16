"""Simple filter, might be obsolete"""
from django.forms import (Form, BooleanField)


class FilterForm(Form):
    output = BooleanField(required=False, initial=True)
