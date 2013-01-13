from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions


from django import forms
from models import Image


class UploadForm(forms.Form):
    file = forms.ImageField(label='Select photo to upload')
    artist = forms.ModelChoiceField(User.objects.all(), required=False)

    class Meta:
        model = Image


class ArtistForm(forms.Form):

    gallery = forms.ModelChoiceField(User.objects.all())

    class Meta:
        model = Image


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'artist',
            ),
            FormActions(Submit('save_changes', 'Save', css_class="btn-primary"))
        )
        super(ImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        fields = ('artist', )
