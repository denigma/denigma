from django.forms import ModelForm, CharField, Textarea, FileField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from models import Profile, Signature, Set


class ProfileForm(ModelForm):
    data_text = CharField(widget=Textarea(attrs={'cols': 80, 'rows': 20}))
    file = FileField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Please provide the data in tab-separated format. First column should be the header. '
                'Provide a column with SEQ_ID, PROBE_ID and PM, for gene and probe id as well as'
                'intensity',
                'name',
                'species',
                'tissue',
                'diet',
                'file',
                'data_text'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        exclude = ('replicates',)


class SignatureForm(ModelForm):
    file = FileField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                "Please provide the data in tab-separated format. First column should be the header. "
                "Provide a column with seq_id, symbol, exp, ctr, fold_change, and p_value. "
                "Any column containing individual expression values from replicates should be prefixed "
                "in the header with exp<nubmer> and ctr<number> corresponding to experimental and control group. "
                "Information can be inferred from the file name. "
                "For this the file name should contain a mapping (attribute1=value1;attribute2=value2...). "
                "Be patient as the upload can take some time.", #  Add a link which opens up a new window and refer to there for checking out progress.
                'name',
                'file',
                'profiles',
                'species',
                'tissues',
                'diet',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(SignatureForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Signature
        exclude = ('transcripts', 'genes')


class SetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset("", 'name', 'signatures'),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Submit('cancel', 'Cancel')
            )
        )
        super(SetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Set
