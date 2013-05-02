from django.forms import Form, ModelForm, CharField, ModelChoiceField, ModelMultipleChoiceField # Textarea,
#from django.utils.translation import ugettext_lazy as _
#from django.conf import settings
#from django.contrib import admin as
#from django.contrib.admin.widgets import FilteredSelectMultiple

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from pagedown.widgets import PagedownWidget

#from ajax_filtered_fields.forms import AjaxManyToManyField, ManyToManyByLetter, ManyToManyByRelatedField

from add.forms import MultipleSelectWithPop #SelectWithPop,
from media.models import Image
from datasets.models import Reference

from models import Entry, Relation, Category


#lookups = (
#    ('images', {'url': 'value'}),
#)


class EntryForm(ModelForm):
    #widgets = {'<attribute_name': Textarea(attrs={'class':'wmd-input', 'id': 'wmd-inout'})} #http://stackoverflow.com/questions/8459967/pagedownmarkdown-editor-with-django
    text = CharField(widget=PagedownWidget(
        attrs={'rows': 10, 'cols': 10,
               'style': 'font-family: monospace',
               #'class':'wmd-input', 'id': 'wmd-input'
        }),
        help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html">reStructuredText Quick Reference</a>\
     | <a href="http://daringfireball.net/projects/markdown/basics">Markdown Basics</a></p>')
    comment = CharField(help_text='Optional, used for revision control.',
        required=False)
#    references = ModelMultipleChoiceField(
#        label= 'References',
#        queryset=Reference.objects.all(),
#        required=False,
#        help_text='References to the literature.',
#        widget=admin.widgets.FilteredSelectMultiple('references', False)
#    )
    #images = forms.ModelMultipleChoiceField(Image.objects, required=False, widget=FilteredSelectMultiple(verbose_name="Images", is_stacked=True,)) # field_name="url",
    #images = ManyToManyByLetter(Image, field_name="url")
    images = ModelMultipleChoiceField(Image.objects, required=False, widget=MultipleSelectWithPop)
    #parent = ModelChoiceField(Entry.objects, widget=SelectWithPop)
    def __init__(self, *args, **kwargs):
        #print(settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js")
        #print(settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js")
        #print(settings.STATIC_ROOT + 'jquery.js')
        #print(settings.STATIC_URL + 'ajax_filtered_fields.js')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'title','text', 'tags', 'categories', 'parent', 'url',
                    'images', 'published', 'comment'),
            FormActions(Submit('save', 'Save', css_class="btn-primary"),
                        Submit('cancel', 'Cancel', css_class="btn-danger")
            )
        )
        super(EntryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Entry
        exclude = ('slug', 'creator', 'updates', 'publisher', 'pub_date', 'tagged', 'html', 'brief_html')
        #widgets = {'images': FilteredSelectMultiple(verbose_name="Images", is_stacked=True,)}
#
#    class Media:
#        js = (
#           # '/admin/jsi18n/',
#            settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
#            settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
#            settings.ADMIN_MEDIA_PREFIX + 'js/jquery.js',
#            settings.STATIC_URL + 'js/ajax_filtered_fields.js',
#        )
#       # css = {'all':[settings.ADMIN_MEDIA_PREFIX + 'css/widgets.css', settings.ADMIN_MEDIA_PREFIX + 'css/uid-manage-forms.css']}


class RelationForm(ModelForm):
    comment = CharField(help_text='Optional, used for revision control.',
        required=False)
    #fr = ModelChoiceField(Entry.objects, widget=SelectWithPop)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'fr', 'be', 'to', 'comment'),
            FormActions(Submit('save', 'Save', css_class="btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn-danger"))
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
                Submit('cancel', 'Cancel', css_class="btn-danger"))
        )
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category


class DeleteForm(Form):
    comment = CharField(help_text='Provide a reason why it is obsolete.',
        required=False)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('', 'comment'),
            FormActions(Submit('delete', 'Delete', css_class="btn-primary"),
                        Submit('cancel', 'Cancel', css_class="btn-danger"))
        )
        super(DeleteForm, self).__init__(*args, **kwargs)


#234567891123456789212345678931234567894123456789512345678961234567897123456789