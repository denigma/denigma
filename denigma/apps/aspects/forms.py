from django.forms import ModelForm, CharField
from models import Hierarchy, HierarchyType, Rank, Grade, Title

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions


class AchievementForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'symbol',
                'requirement',

            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel'),
            )
        )

        super(AchievementForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HierarchyType


class HierarchyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'description',
                'symbol',
                'requirement',
                'type',
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel'),
            )
        )

        super(HierarchyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Hierarchy


class RankForm(HierarchyForm):
    class Meta:
        model = Rank


class GradeForm(HierarchyForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'symbol',
                'requirement',
                'type',
                'language',
            ),
            FormActions
        )
        FormActions(
            Submit('save', 'Save', css_class="btn-primary"),
            Submit('cancel', 'Cancel')
        )
        super(GradeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Grade



class TitleForm(HierarchyForm):
    class Meta:
        model = Title