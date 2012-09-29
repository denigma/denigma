from django.forms import ModelForm, CharField, Textarea

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from models import Species, Tissue


class SpeciesForm(ModelForm):
    comment = CharField(required=False)
    description = CharField(widget=Textarea(attrs={'cols': 10,'rows': 5}))
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'common_name',
                'short_name',
                'latin_name',
                'taxid',
                'description',
                'complexity',
                'main_model',
                'alternative_names',
                'images',
                'comment'
            ),
            FormActions(
                Submit('save_species', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(SpeciesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Species
        exclude = ('number_genes', 'gendr_genes', 'gendr_paralogs', 'gendr_orthologs',
                    'short_latin_name')

class TissueForm(ModelForm):
    comment = CharField(required=False)
    synonyms = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'synonyms',
                'description',
                'hierarchy',
                'images',
                'comment'

            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(TissueForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Tissue
        exclude = ('identifier', 'notes',)

class DeleteTissueForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Please confirm deletion and comment on the reason why it is obsolete',
                'comment'
            ),
            FormActions(
                Submit('delete', 'Delete'),
                Submit('cancel', 'Cancel', css_class="btn-primary")
                )
        )
        super(DeleteTissueForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tissue
        fields = ('comment',)
