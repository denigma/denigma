from django.forms import Form, ModelForm, CharField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from add.forms import MultipleSelectWithPop
from data.models import Entry
from experts.models import Profile

from models import Link, Category, Country


class LinkForm(ModelForm):
    comment = CharField(required=False)
    category = ModelMultipleChoiceField(Category.objects.all().order_by('title'), required=False, widget=MultipleSelectWithPop)
    categories = ModelMultipleChoiceField(Entry.objects.all().order_by('title'), required=False, widget=MultipleSelectWithPop)
    countries = ModelMultipleChoiceField(Country.objects, required=False, widget=MultipleSelectWithPop)
    contacts = ModelMultipleChoiceField(Profile.objects.all().order_by('user_name'), required=False, widget=MultipleSelectWithPop)
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
                'categories',
                'language',
                'countries',
                'contact',
                'contacts',
                'site',
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
        fields = ('title', 'description', 'url', 'category', 'categories', 'language', 'countries', 'contact', 'contacts', 'site', 'comment')


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


class CountryForm(ModelForm):
    comment = CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'abbreviation',
                'name',
                )
            )
        FormActions(
            Submit('save', 'Save', css_class="btn-primary"),
            Submit('cancel', 'Cancel', css_class="btn-danger")
        )
        super(CountryForm, self).__init__(*args, **kwargs)

    class Meta():
        model = Country


class FilterForm(Form):
    filter = CharField()

