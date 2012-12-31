from django.forms import ModelForm, CharField, ModelChoiceField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from add.forms import SelectWithPop, MultipleSelectWithPop
from data.models import Entry
from links.models import Link

from models import Profile, Collaboration


class ProfileForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('',
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'affiliation',
                'country',
                'state',
                'city',
                'street',
                'zip_code',
                'website',
                'phone',
                'mobile',
                'msn',
                'birthday',
                'gender',
                'work',
                'publications',
                'collaboration',
                'entries',
                'comment'
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn btn-danger")),
        )
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        exclude = ('working_hours', 'business_hours', 'user', 'password', 'user_name')


class CollaborationForm(ModelForm):
    comment = CharField(required=False)
    project = ModelChoiceField(Entry.objects, required=True, widget=SelectWithPop)
    labs = ModelMultipleChoiceField(Link.objects.filter(category__title__icontains='Research'), required=True, widget=MultipleSelectWithPop)
    members = ModelMultipleChoiceField(Profile.objects, required=True, widget=MultipleSelectWithPop)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'project', 'labs', 'members', 'comment'),
        FormActions(
            Submit('save', 'Save', css_class="btn-primary"),
            Submit('cancel', 'Cancel', css_class="btn-danger")
        ))
        super(CollaborationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Collaboration
        fields = ('project', 'labs', 'members')