from django import forms
from django.contrib import admin

import reversion

from models import Post


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':30,
                                                               'cols':80,
                                                               'style':'font-family:monospace'}),
                                                               help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html">reStructuredText Quick Reference</a>')
    class Meta:
       model = Post


class PostAdmin(reversion.VersionAdmin):
    list_display = ('title', 'brief', 'tagged', 'created', 'updated', 'published')
    list_filter = ['created', 'updated', 'tags__name']
    fields = ('title', 'text', 'tags', 'images', 'published')

    form = PostAdminForm  

    def tagged(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    tagged.allow_tag = True


admin.site.register(Post, PostAdmin)
