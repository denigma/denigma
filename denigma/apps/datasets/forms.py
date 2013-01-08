from django.forms import Form, ModelForm, CharField, FileField, Textarea, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from data.models import Entry
from add.forms import MultipleSelectWithPop
from models import Reference


class FilterForm(Form):
    filter = CharField()


class UploadForm(Form):
    file = FileField(label='Select reference article to upload')


class ReferenceForm(ModelForm):
    notes = CharField(widget=Textarea, required=False)
    categories = ModelMultipleChoiceField(Entry.objects.all().order_by('title'), required=False, widget=MultipleSelectWithPop)
    comment = CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Either a PMID or a title is totally sufficient to create a reference.',
                'pmid', 'title', 'notes', 'label', 'categories', 'comment'),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(ReferenceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Reference
        fields = ('pmid', 'title', 'notes', 'label', 'categories')

