"""Simple filter, might be obsolete"""
from django.forms import (Form, BooleanField, ModelForm, MultipleChoiceField)

# from lifespan.models import Variant


class FilterForm(Form):
    output = BooleanField(required=False, initial=True)


# class VariantForm(ModelForm):
#     ethnicity = MultipleChoiceField()
#
#     class Meta:
#         model = Variant
#         fields = ('ethnicity')