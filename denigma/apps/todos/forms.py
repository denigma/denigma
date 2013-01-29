from datetime import datetime
from django.forms import ModelForm, DateTimeField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from models import Todo


class TodoForm(ModelForm):
    start_date = DateTimeField(initial=datetime.now(), required=False)
    stop_date = DateTimeField(initial=datetime.now(), required=False)
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