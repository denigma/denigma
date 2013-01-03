from django.contrib.auth.models import User

from django import forms
from models import Image

class UploadForm(forms.Form):
    file = forms.ImageField(label='Select photo to upload')
    artist = forms.ModelChoiceField(User.objects.all(), required=False)

    class Meta:
        model = Image

class ArtistForm(forms.Form):
    gallery = forms.ModelChoiceField(User.objects.all())

    class Mets:
        model = Image