from datetime import datetime

from django.forms import ModelForm, DateTimeField, ModelMultipleChoiceField
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from data.models import Entry
from add.forms import MultipleSelectWithPop

from models import Todo


class TodoForm(ModelForm):
    start_date = DateTimeField(initial=datetime.now(), required=False, help_text="Optional")
    stop_date = DateTimeField(initial=datetime.now(), required=False, help_text="Optional")
    categories = ModelMultipleChoiceField(Entry.objects.all().order_by('title'), required=False, widget=MultipleSelectWithPop, help_text="The categories which this todo belongs to. It also be used to assign arbitrary kind of labels")
    executor = ModelMultipleChoiceField(User.objects.all().order_by('username'), required=False, help_text="The assigned user who should execute the todo (Optional).")
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'priority',
                'value',
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