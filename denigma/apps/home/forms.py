import re
from django import forms

from blog.models import Post

class DynamicForm(forms.Form):
    """Initialize form values from views."""
    select = forms.BooleanField(label='', required=False)
    field_1 = forms.CharField(label='', widget=forms.TextInput(attrs=\
        {'size': '20', 'readonly': 'readonly'}))
    field_2 = forms.ChoiceField(widget=forms.Select(),\
        choices=((post.id, post.title) for post in Post.objects.all()))

    def __init__(self, *args, **kwargs):
        super(DynamicForm, self).__init__(*args, **kwargs)
        input = kwargs.get('inital', {})
        get_field_1_initial_input_from_views = re.sub("[|\]|u'|'", "", str(input.values()))

        # Override field_2 choices based on field_1 input
        try:
            # filter choices
            self.fields['fields_2'].choices((post.id, post.title) for post in Post.objects.filter(id=1))
        except:
            pass
