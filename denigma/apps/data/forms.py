from django.forms import ModelForm, CharField, Textarea
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from models import Entry, Relation, Tag, Category


class EntryForm(ModelForm):
    text = CharField(widget=Textarea(
        attrs={'rows': 10, 'cols': 10,
               'style': 'font-family: monospace'}),
        help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html">reStructuredText Quick Reference</a>\
     | <a href="daringfireball.net/projects/markdown/basics">Markdown Basics</a></p>')
    comment = CharField(help_text='Optional, used for revision control.',
        required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'title','text', 'tags', 'categories', 'parent', 'url',
                    'images', 'published', 'comment'),
            FormActions(Submit('save', 'Save', css_class="btn-primary"),
                        Submit('cancel', 'Cancel')
            )
        )
        super(EntryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Entry
        exclude = ('slug', 'creator', 'updates', 'publisher', 'pub_date', 'tagged')


class RelationForm(ModelForm):
    comment = CharField(help_text='Optional, used for revision control.',
        required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'fr', 'be', 'to', 'comment'),
            FormActions(Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel'))
        )
        super(RelationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Relation
        exclude = ('creator', 'updates')

class CategoryForm(ModelForm):
    comment = CharField(help_text='Optional, used for revision control.',
        required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'name', 'definition', 'synonyms', 'comment'),
            FormActions(Submit('save', 'Save', css_class='btn-primary'),
                Submit('cancel', 'Cancel'))
        )
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category

#234567891123456789212345678931234567894123456789512345678961234567897123456789