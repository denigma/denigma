from datetime import datetime
from django.forms import ModelForm, DateTimeField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from data.models import Entry
from add.forms import MultipleSelectWithPop
from profiles.models import Profile

from models import Todo


class TodoForm(ModelForm):
    start_date = DateTimeField(initial=datetime.now(), required=False)
    stop_date = DateTimeField(initial=datetime.now(), required=False)
    categories = ModelMultipleChoiceField(Entry.objects.all().order_by('title'), required=False, widget=MultipleSelectWithPop)
    executor = ModelMultipleChoiceField(Profile.objects.all().order_by('name'), required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'importance',
                'difficulty',
                'progress',
                'start_date',
                'stop_date',
                'creator',
                'executor',
                'categories',
                'onhold',
                'done',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )

        super(TodoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Todo