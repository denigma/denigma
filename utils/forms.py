from django.forms import ModelForm


class RequestModelForm(ModelForm):
    """Sub-class the ModelForm to provide an instance of `request`.
    It also saves the object with the appropriate user."""
    def __init__(self, request, *args, **kwargs):
        """Overwrite init to grap the request object."""
        self.request = request
        super(RequestModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(RequestModelForm, self).save(commit=False)
        m.owner =self.request.user
        if commit:
            m.save()
        return m