# -*- coding: utf-8 -*-
from django.forms import (Form, ModelForm, CharField, Textarea, IntegerField, BooleanField,
                          ModelChoiceField, ModelMultipleChoiceField)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from django_easyfilters import FilterSet

from annotations.models import Species
from datasets.models import Reference
from add.forms import SelectWithPop, MultipleSelectWithPop

from models import (Study, Experiment, Measurement, Comparison, Intervention, Factor,\
                   Strain, Epistasis, Regimen, Assay, Manipulation,
                   Variant, Population, State, Technology, StudyType, Type, VariantType, ORType)

from annotations.models import Classification

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
                Submit('cancel', 'Cancel', css_class="btn-danger"),
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
                Submit('delete_study', 'Delete study', css_class="btn-warning"),
                Submit('delete_reference', 'Delete study & reference', css_class="btn-danger"),
                Submit('cancel', 'Cancel', css_class="btn-primary")
                )
        )
        super(DeleteStudyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Study
        fields = ['comment']


class DeleteInterventionForm(ModelForm):
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
                Submit('delete', 'Delete', css_class="btn-danger"),
                Submit('cancel', 'Cancel', css_class="btn-primary")
                )
        )
        super(DeleteInterventionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Intervention
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
                Submit('delete_experiment', 'Delete experiment', css_class="btn-danger"),
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
    assay = ModelChoiceField(queryset=Assay.objects.all())
    comment = CharField(help_text="Optional, for version-control.", required=False)
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
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'name', 'data', 'study', 'species', 'assay', 'comment'),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
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
        fields = ['name', 'data', 'study', 'species', 'assay']


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement


class ComparisonForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'intervention',
                'epistasis',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(ComparisonForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Comparison
        fields = ('epistasis', 'intervention')


class InterventionForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'taxid',
                'species',
                'sex',
                'gender',
                'background',
                'strain',
                'effect',
                'mean',
                'median',
                'maximum',
                '_25',
                '_75',
                'manipulation',
                'pmid',
                'references',
                'lifespans', #Depricated?
                'comment',
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(InterventionForm, self).__init__(*args, **kwargs)

    def clean_references(self):
        pmid = self.cleaned_data.get('pmid', None)
        clean_references = [reference for reference in self.cleaned_data.get('references', [])]
        if pmid:
            reference, created = Reference.objects.get_or_create(pmid=pmid)
            clean_references.append(reference)
        return clean_references

    class Meta:
        model = Intervention


class FactorForm(ModelForm):
    species = ModelChoiceField(queryset=Species.objects.all().order_by('-main_model', 'complexity'),
        required=False)
    comment = CharField(required=False)
    intervention = ModelMultipleChoiceField(Intervention.objects, required=False, widget=MultipleSelectWithPop)
    classifications = ModelMultipleChoiceField(Classification.objects, required=False, widget=MultipleSelectWithPop)

    try: assay = ModelMultipleChoiceField(Assay.objects, initial=[Assay.objects.get(name__startswith='Orga')])
    except Exception as e:
        print(e)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'symbol',
                'name',
                'alias',
                'entrez_gene_id',
                'ensembl_gene_id',
                'pdb',
                'taxid',
                'species',
                'observation',
                'assay',
                'intervention',
                'classifications',
                'function',
                'mean',
                'median',
                'maximum',
                'pubmed_id',
                'references',
                'types',
                'note',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(FactorForm, self).__init__(*args, **kwargs)

    def clean_references(self):
        pmid = self.cleaned_data.get('pmid', None)
        clean_references = [reference for reference in self.cleaned_data.get('references', [])]
        if pmid:
            reference, created = Reference.objects.get_or_create(pmid=pmid)
            clean_references.append(reference)
        return clean_references

    class Meta:
        model = Factor
        fields = ('symbol', 'name', 'alias', 'entrez_gene_id', 'ensembl_gene_id', 'pdb',
                  'taxid', 'species', 'observation', 'comment',
                  'assay', 'classifications', 'intervention',
                  'function', 'mean','median','maximum',
                  'pubmed_id', 'references','types', 'note')


class VariantForm(ModelForm):
    comment = CharField(required=False)
    factor = ModelChoiceField(Factor.objects, required=False, widget=SelectWithPop)
    choice = ModelChoiceField(State.objects, required=False, widget=SelectWithPop)
    ethnicity = ModelMultipleChoiceField(Population.objects, required=False, widget=MultipleSelectWithPop)
    technology = ModelChoiceField(Technology.objects, required=False, widget=SelectWithPop)
    study_type = ModelChoiceField(StudyType.objects, required=False, widget=SelectWithPop)
    variant_type = ModelChoiceField(VariantType.objects, required=False, widget=SelectWithPop)
    or_type = ModelChoiceField(ORType.objects, required=False, widget=SelectWithPop)
    reference = ModelChoiceField(Reference.objects, required=False, widget=SelectWithPop)
    try:
        classifications = ModelMultipleChoiceField(Classification.objects, required=False, widget=MultipleSelectWithPop,
                                               initial=[Classification.objects.get(title__startswith='Longevity-Associated')])
    except Exception as e:
        print(e)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'polymorphism',
                'alias',
                'variant_type',
                'location',
                'factor',
                'factors',
                'description',
                'finding',
                'odds_ratio',
                'or_type',
                'pvalue',
                'p_value',
                'qvalue',
                'significant',
                'classifications',
                'initial_number',
                'replication_number',
                'ethnicity',
                'age_of_cases',
                'technology',
                'study_type',

                'shorter_lived_allele',
                'longer_lived_allele',
                'pmid',
                'reference',
                'choice',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(VariantForm, self).__init__(*args, **kwargs)

    def clean_reference(self):
         print("cleaning references")
         pmid = self.cleaned_data.get('pmid', None)
         if pmid:
             reference, created = Reference.objects.get_or_create(pmid=pmid)
             print reference, created
         else:
             reference = self.cleaned_data.get('reference', None)
         return reference

    class Meta:
        model = Variant
        fields = ('polymorphism', 'alias', 'variant_type', 'location', 'factor', 'factors', 'description', 'finding', 'choice', 'classifications',
                  'odds_ratio', 'or_type', 'pvalue', 'p_value', 'qvalue', 'significant', 'initial_number',
                  'replication_number', 'ethnicity', 'age_of_cases', 'technology', 'study_type',
                  'shorter_lived_allele', 'longer_lived_allele', 'pmid', 'reference', 'comment')


#234567891123456789212345678931234567894123456789512345678961234567897123456789

# Auxillary:
class StrainForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'species',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(StrainForm, self).__init__(*args, **kwargs)

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

class StateForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(StateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = State

class TechnologyForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(TechnologyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Technology


class StudyTypeForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(StudyTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudyType


class PopulationForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(PopulationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Population

class VariantTypeForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(VariantTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = VariantType


class ORTypeForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(ORTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ORType


class VariantBulkInsertForm(Form):
    data = CharField(label='data', widget=Textarea(attrs={'cols': 20, 'rows': 20}))
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Please provide a tab separeted list of the varaints (copied from an spreadsheet for instance) with the following fields in the header as first line:\n'
                '"Choice" "PMID" "Link" "Gene symbol (HGNC)" "Entrez Gene ID" "Polymorphism" "Shorter-lived allele" "Odds ratio" "P value" "Significant?" "Number of cases / controls (initial study)" "Ethnicity" "Age of cases" "Number of cases/controls (replication study)" "Technology" "Study type" "Notes" "Finding" "Variant type" "OR type" (An optional "Longer-lived allele" field might be included right after the "Shorter-lived allele" field)',
                'data',
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(VariantBulkInsertForm, self).__init__(*args, **kwargs)


class OntologyForm(Form):
    classifications = ModelMultipleChoiceField(Classification.objects, required=False)
    species = ModelMultipleChoiceField(Species.objects, required=False)
    types = ModelMultipleChoiceField(Type.objects, required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'classifications',
                'species',
                'types',
            ),
            FormActions(
                Submit('Query', 'Query', css_class="btn-primary")
            )
        )
        super(OntologyForm, self).__init__(*args, **kwargs)



class FilterForm(Form):
    filter = CharField()


class FactorFilterSet(FilterSet):
    fields = ['species', 'classifications', 'types']

class InterventionFilterSet(FilterSet):
    fields = ['species', 'manipulation']


class VariantFilterSet(FilterSet):
    fields = ['classifications', 'study_type', 'variant_type', 'or_type', 'significant', 'finding', 'created', 'updated'] #, 'location'] #, 'choice', 'ethnicity',  'technology']