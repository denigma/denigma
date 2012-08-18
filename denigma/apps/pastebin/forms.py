from django import forms
from django.utils.translation import ugettext_lazy as _

from models import PastedItem


class PastedItemForm(forms.ModelForm):
    class Meta():
        model = PastedItem
        fields = ('text', )

    def __init__(self, user = None, *args, **kwargs):
        self.user = user
        super(PastedItemForm, self).__init__(*args, **kwargs)
