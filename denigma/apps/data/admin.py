from django.contrib import admin
from django.db import models
from django import forms

import reversion
from pagedown.widgets import AdminPagedownWidget

from datasets.models import Reference

from models import Entry, Change, Relation, Alteration, Category, Tag


#class ChangeInline(admin.StackedInline):
#    model = Change
#    fk_name = 'of'
#
#class RelationInline(admin.StackedInline):
#    model = Relation
#    fk_name = 'fr'
#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.request = request
#        obj.save()


class EntryAdminForm(forms.ModelForm):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    text = forms.CharField(widget=AdminPagedownWidget(
        attrs={'rows': 30, 'cols': 80, 'style': 'font-family:monospace'}),
        help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/'
                  'quickref.html">reStructuredText Quick Reference</a>'
    )
    references = forms.ModelMultipleChoiceField(
        label='References',
        queryset=Reference.objects.all(),
        required=False,
        help_text='References to the literature.',
        widget=admin.widgets.FilteredSelectMultiple('references', False)
    )


class EntryAdmin(reversion.VersionAdmin):
    search_fields = ('title', 'text', 'url')
    ordering = ('-created',)
    list_filter = ('published',)
    #inlines = [ChangeInline]
    #inlines = [RelationInline]
    filter_horizontal = ('categories', 'images')
    form = EntryAdminForm


    def save_model(self, request, obj, form, change):
        print("EntryAdmin.save_model here!")
        obj.user = request.user
        obj.request = request
        obj.save()

        obj.references.clear()
        for reference in form.cleaned_data['references']:
            obj.references.add(reference)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['references'].initial = [o.pk for o in obj.references.all()]
        else:
            self.form.base_fields['references'].intial = []
        return super(EntryAdmin, self).get_form(request, obj, **kwargs)


class RelationAdmin(reversion.VersionAdmin):
    ordering = ('-created',)
    def save_model(self, request, obj, form, change):
        print("RelationAdmin.save_model here!")
        obj.user = request.user
        obj.save()


class ChangeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')
    ordering  = ('-at',)
    list_filter = ('by',)


class AlterationAdmin(admin.ModelAdmin):
    ordering = ('at',)


class CategoryAdmin(reversion.VersionAdmin):
    ordering = ('name',)


class TagAdmin(reversion.VersionAdmin):
    ordering = ('name',)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Alteration, AlterationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)