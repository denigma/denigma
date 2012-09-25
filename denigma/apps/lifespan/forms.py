from django.forms import ModelForm, CharField, Textarea, BooleanField, ModelChoiceField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from models import (Study, Experiment, Measurement, Comparision, Intervention, Factor,\
                   Strain, Epistasis, Regimen, Assay, Manipulation)

from annotations.models import Species


# Main:
class StudyForm(ModelForm):
    title = CharField(label='Titles', widget=Textarea(attrs={'cols': 20, 'rows': 20}))
    pmid = CharField(label="PMIDs", widget=Textarea(attrs={'cols': 80, 'rows': 20}))
    comment = CharField()

    class Meta:
        model = Study
        fields = ('title', 'pmid', 'species', 'comment')


class EditStudyForm(ModelForm):
    comment = CharField(required=False)
    species = ModelMultipleChoiceField(queryset=Species.objects.all().order_by('-main_model', 'complexity'))
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Check whether this study is correctly integrated into Denigma.</b>',
                'title',
                'pmid',
                'link',
                'reference',
                'species',
                'notes',
                'comment',
                'integrated'
            ),
            #Field('title', css_class='input-xlarge'),
            #Field('checkboxes', style="background: #FAFAFA; padding:10px"),
            #PrependedField('integrated', '<input type="checkbox" unchecked="unchecked" value="" id="" name="">', active=True),
            #PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
            #ButtonHolder(Submit('submit', 'Submit', css_class='button white'),),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Submit('cancel', 'Cancel'),
            )
        )

        super(EditStudyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Study
        #fields = ('title', 'pmid', 'link', 'reference', 'species', 'notes')#, 'integrated')


class DeleteStudyForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Please confirm deletion and comment on the reason why it is obsolete.',
                'comment'),
            Field('text_input', css_class='input-xlarge'),
            FormActions(
                Submit('delete_study', 'Delete study'),
                Submit('delete_reference', 'Delete study & reference'),
                Submit('cancel', 'Cancel', css_class="btn-primary")
                )
        )
        super(DeleteStudyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Study
        fields = ['comment']


class DeleteExperimentForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Please confirm deletion and comment on the reason why it is obsolete',
                'comment'),
            Field('tet_input', css_class='input-xlarge'),
            FormActions(
                Submit('delete_experiment', 'Delete experiment'),
                Submit('cancel', 'Cancel', css_class="btn-primary")
            )
        )
        super(DeleteExperimentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Experiment
        fields = ['comment']


class ExperimentForm(ModelForm):
    name = CharField(help_text="(Use the figure or table title as name for the experiment)")
    study = ModelChoiceField(queryset=Study.objects.all())
    species = ModelChoiceField(queryset=Species.objects.all().order_by('-main_model', 'complexity'))
    data = CharField(widget=Textarea(attrs={'cols': 160, 'rows': 20,
                                            'style': 'font-family: monospace'}),
        help_text="(space or tab-seperated header + blank line + series of measurements)",
        initial="""genotype treatment mean median max num pvalue
#temperature=22

wt AL 20 25 30 50\nwt DR 24 29 32 50 <0.01
mutant DR 20 25 30 50 1 >0.05
# Other meta data like type of statistical test.""")

    def __init__(self, *args, **kwargs):
        """Overwritting initializer to set default study and species."""
        if 'pk' in kwargs:
            pk = kwargs['pk']
            del kwargs['pk']
        super(ExperimentForm, self).__init__(*args, **kwargs)
        if 'pk' in locals() and pk:
            all_studies = Study.objects.all()
            study_query_set = all_studies.filter(pk=pk)
            species_query_set = Species.objects.all()
            species = study_query_set[0].species.all()
            if len(species) == 1:
                initial = species[0].pk
            else:
                initial = None
            self.fields['study'] = ModelChoiceField(queryset=all_studies, initial=study_query_set[0])
            self.fields['species'] = ModelChoiceField(queryset=species_query_set, initial=initial)

    class Meta:
        model = Experiment
        fields = ['name', 'data', 'study', 'species']


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement


class ComparisionForm(ModelForm):
    class Meta:
        model = Comparision


class InterventionForm(ModelForm):
    class Meta:
        model = Intervention


class FactorForm(ModelForm):
    class Meta:
        model = Factor


# Auxillary:
class StrainForm(ModelForm):
    class Meta:
        model = Strain


class EpistatisForm(ModelForm):
    class Meta:
        model = Epistasis


class RegimenForm(ModelForm):
    class Meta:
        model = Regimen


class AssayForm(ModelForm):
    class Meta:
        model = Assay


class ManipulationForm(ModelForm):
    class Meta:
        model = Manipulation
