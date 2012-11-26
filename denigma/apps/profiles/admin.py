from django.contrib import admin
from django import forms

from models import Profile

from aspects.models import Rank, Grade, Title, Role


def profile_form_factory(profile):
    class ProfileForm(forms.ModelForm):
        rank = forms.ModelChoiceField(queryset=Rank.objects.all(), initial=profile.rank, required=False)
        grades = forms.ModelMultipleChoiceField(Grade.objects.all(), initial=profile.grades.all(), required=False)
        title = forms.ModelChoiceField(queryset=Title.objects.all(), initial=profile.title, required=False)
        role = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), initial=profile.role.all(), required=False)

        class Meta:
            model = Profile

    return ProfileForm


class ProfileAdmin(admin.ModelAdmin):
    pass

    def get_form(self, request, obj=None, **kwargs):
        self.form = profile_form_factory(obj)
        return super(ProfileAdmin, self).get_form(request, obj, **kwargs)

    def save_form(self, request, form, **kwargs):
        print("form saving")
        #form.save(commit=False)
        print form
        print("rank %s" % form.fields['rank'])
        #print form.get_cleaned_data
        print("title %s" % form.fields['title'])
        return super(ProfileAdmin, self).save_form(request, form, **kwargs)

    def save_model(self, request, obj, form, change):
        #print("save_model")
        cd = form.cleaned_data
        obj.rank = cd['rank']
        obj.title = cd['title']
        super(ProfileAdmin, self).save_model(request, obj, form, change)


admin.site.register(Profile, ProfileAdmin)

