from random import random
import re

from django import forms
from django.utils.hashcompat import sha_constructor

from shorty.models import *


class CSVField(forms.CharField):
    def __init__(self, *args, **kw):
        self.each_max = kw.pop('each_max', 50)
        super(CSVField, self).__init__(*args, **kw)

    def check_max(self, value):
        if len(value) > self.each_max:
            raise ValidationError("individual value longer than %d" % self.each_max)
        return value

    def clean(self, value):
        cleaned_value = super(CSVField, self).clean(value)
        return [self.check_max(data.strip()) for data in cleaned_value.strip().split(',')]

class SourceForm(forms.ModelForm):
    class Meta:
        model = SourceURL

    labels = CSVField(each_max=50, widget=forms.TextInput, required=True)

    def save(self, **kw):
        source = super(SourceForm, self).save(commit=False, **kw)
        salt = sha_constructor(str(random())).hexdigest()[:5]

        email = self.cleaned_data['email']
        url = self.cleaned_data['url']

        admin_key = sha_constructor("|".join([salt, email, url])).hexdigest()
        source.admin_key = admin_key

        labels = self.cleaned_data['labels']

        source.save()
        for label in labels:
            shorty = ShortyURL(source=source, label=label).save()

        return source
