from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

try:
    from notification import models as notification
except ImportError:
    notification = None

from models import Announcement


class AnnouncementAdminForm(forms.ModelForm):
    """A custom form for the admin of the Announcement model. Has an extra field
    called send_now that when checked will send out the announcement allowing
    the user to decide when that happens."""
    send_now = forms.BooleanField(required=False,
        help_text=_("Tick this box to send out this announcement now."))

    users = forms.ModelMultipleChoiceField(User.objects.all(), required=False)

#http://stackoverflow.com/questions/11657682/django-admin-interface-using-horizontal-filter-with-inline-manytomany-field
#    creator = forms.ModelMultipleChoiceField(
#        queryset=User.objects.all(),
#        required=False,
#        widget=FilteredSelectMultiple(verbose_name="User profile",
#        is_stacked=False))
#
#    def __init__(self, *args, **kwargs):
#        super(AnnouncementAdminForm, self).__init__(*args, **kwargs)
#        if self.instance.pk:
#            self.fields['userproifles'].initial = self.instance.creator

    class Meta:
        model = Announcement
        exclude = ("creator", "creation_date")

    def save(self, commit=True):
        """Checks the send_now field in the form and when True sends out the
        announcement through notification if present."""

        announcement = super(AnnouncementAdminForm, self).save(commit)
        if self.cleaned_data["send_now"]:
            if notification:
                users = User.objects.all()
                notification.send(users, "announcement", {
                    "announcement": announcement,
                    }, on_site=False, queue=True)
        if self.users: print(users)
        return announcement


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = [
            "title",
            "content",
            "site_wide",
            "members_only",
            "dismissal_type",
            "publish_start",
            "publish_end"
        ]

from django.contrib.auth.models import User

try:
    from profiles.models import Profile as profiles
except ImportError as e:
    profiles = None
    print(e)
#try:
#    from experts.models import Profile as experts
#except ImportError as e:
#    experts = None
#    print(e)


class UserForm(forms.Form):
#    text = forms.CharField()
#    users = forms.ModelMultipleChoiceField(User.objects.all())
    try:
        profiles = forms.ModelMultipleChoiceField(profiles.objects.all(), required=False)
    except Exception as e:
        pass
        print(e)
#    try:
#        experts = forms.ModelMultipleChoiceField(experts.objects.all(), required=False)
#    except Exception as e:
#        pass
#        print(e)