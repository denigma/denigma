from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import PastedItem

try:
    from notification import models as notification
except ImportError:
    notification = None 


class PastedItemForm(forms.ModelForm):
    class Meta():
        model = PastedItem
        fields = ('text', )

    def __init__(self, user = None, *args, **kwargs):
        self.user = user
        super(PastedItemForm, self).__init__(*args, **kwargs)


class SendItemForm(forms.Form):
    """Form that deals with submitted data."""
    uuid = forms.CharField(max_length=36)
    recipient = forms.CharField(max_length=30)

    def __init__(self, sender=None, *args, **kwargs):
        super(SendItemForm, self).__init__(*args, **kwargs)
        self.sender = sender

    def clean_uuid(self):
        try:
            return PastedItem.objects.get(uuid=self.cleaned_data['uuid'])
        except PastedItem.DoesNotExists:
            raise forms.ValidationError(_("The pasted item was not found."))

    def clean_recipient(self):
        recipient = self.cleaned_data['recipient']
        try:
            return User.objects.get(username=recipient)
        except User.DoesNotExist:
            raise forms.ValidationError("There is no user named %s." % recipient)
    
    def save(self):
        """Will notify the recipient and also the sender."""
        self.pasted_item = self.cleaned_data['uuid']
        self.recipient_user = self.cleaned_data['recipient']
        if notification:
           notification.send([self.sender], "pasteditem_sent",
                              {'pasted_item': self.pasted_item,
                               'recipient': self.recipient_user,})
           notification.send([self.recipient_user], "pasteditem_received", # If the last argument is wrong it raises a NoticeType matching query does not exist.
                              {'pasted_item': self.pasted_item,
                               'sender': self.sender,})

           # Recipients:
#           self.recipients = self.cleaned_data['recipients']
#           if self.recipients:
#                notification.send(self.recipients, 'pasteditem_recieved',
#                                {'pasted_item': self.pasted_item,
#                                'sender': self.sender,})
