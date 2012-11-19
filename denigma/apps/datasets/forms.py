from django.forms import Form, ModelForm, CharField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from models import Reference


class FilterForm(Form):
    filter = CharField()


class ReferenceForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'pmid', 'title', 'notes', 'comment'),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(ReferenceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Reference
        fields = ('pmid', 'title', 'notes')
