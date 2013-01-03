from django.forms import ModelForm, CharField, Textarea, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from add.forms import MultipleSelectWithPop
from media.models import Image

from models import Classification, Tissue, Species, Animal


DELETE_INFO_TEXT = _('Please confirm deletion and comment on the reason why it is obsolete')


class ClassificationForm(ModelForm):
    comment = CharField(required=False, help_text="... on the reason for editing.")
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '', 'title', 'slug', 'abbreviation', 'description', 'parent', 'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(ClassificationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Classification


class TissueForm(ModelForm):
    comment = CharField(required=False, help_text="... on the reason for editing.")
    synonyms = CharField(required=False)
    notes = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '', 'name', 'synonyms', 'description', 'parent', 'hierarchy', 'images', 'notes',  'comment'

            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(TissueForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Tissue
        exclude = ('identifier',)

class DeleteTissueForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                DELETE_INFO_TEXT, _('comment')
            ),
            FormActions(
                Submit('delete', _('Delete'), css_class="btn-danger"),
                Submit('cancel', _('Cancel'), css_class="btn-primary")
            )
        )
        super(DeleteTissueForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tissue
        fields = ('comment',)


class DeleteClassificationForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                DELETE_INFO_TEXT, _('comment')
            ),
            FormActions(
                Submit('delete', _('Delete'), css_class="btn-danger"),
                Submit('cancel', _('Cancel'), css_class="btn-primary")
            )
        )

        super(DeleteClassificationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Classification
        fields = ('comment',)


class SpeciesForm(ModelForm):
    comment = CharField(required=False)
    description = CharField(widget=Textarea(attrs={'cols': 10,'rows': 5}))
    alternative_names = ModelMultipleChoiceField(Animal.objects.all(), required=False, widget=MultipleSelectWithPop)
    images = ModelMultipleChoiceField(Image.objects.all(), required=False, widget=MultipleSelectWithPop)
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
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(SpeciesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Species
        exclude = ('number_genes', 'gendr_genes', 'gendr_paralogs', 'gendr_orthologs',
                    'short_latin_name')

class AnimalForm(ModelForm):
    comment = CharField(required=False)
    class Meta:
        model = Animal
