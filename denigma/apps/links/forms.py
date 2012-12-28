from django.forms import Form, ModelForm, CharField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from add.forms import MultipleSelectWithPop

from models import Link, Category


class LinkForm(ModelForm):
    comment = CharField(required=False)
    category = ModelMultipleChoiceField(Category.objects, required=False, widget=MultipleSelectWithPop)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'url',
                'category',
                'comment',
                ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(LinkForm, self).__init__(*args, **kwargs)

    class Meta():
        model = Link
        fields = ('title', 'description', 'url', 'category', 'comment')


class CategoryForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'comment',
            ),
            FormActions(
                Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta():
        model = Category
        fields = ('title', 'description', 'comment')


class FilterForm(Form):
    filter = CharField()