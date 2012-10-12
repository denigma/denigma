from django.forms import Form, ModelForm, CharField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FormActions

from models import Link


class LinkForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'url',
                'category',
                'comment',
                ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(LinkForm, self).__init__(*args, **kwargs)

    class Meta():
        model = Link
        fields = ('title', 'description', 'url', 'category', 'comment')


class FilterForm(Form):
    filter = CharField()