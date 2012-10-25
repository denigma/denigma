from django.contrib import admin
from django import forms

import reversion

from models import Post, Comment


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows':30,
               'cols':80,
               'style':'font-family:monospace'}),
        help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/'
                  'quickref.html">reStructuredText Quick Reference</a>'
    )
    class Meta:
       model = Post


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('text',)

    def save_model(self, request, obj, form, change, *args, **kwargs):
        if getattr(obj, 'maker', None) is None:
            obj.maker = request.maker
        obj.maker = request.maker
        obj.save()

    def queryset(self, request):
        qs = super(CommentInline, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(maker=request.user)


class PostAdmin(reversion.VersionAdmin):
    list_display = ('title', 'brief', 'tagged', 'created', 'updated', 'creator', 'updater', 'published')
    list_filter = ['created', 'updated', 'published', 'tags__name']
    fields = ('title', 'text', 'tags', 'url', 'images', 'published')
    search_fields = ('title', 'text')#, 'tagged_items')

    form = PostAdminForm  

    inlines = (CommentInline,)

    def save_model(self, request, obj, form, change, *args, **kwargs):
        """Saves the current user as creator and/or updater."""
        print("Saveing post")
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.updater = request.user
        obj.save()

    def tagged(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    tagged.allow_tag = True
    # Redirecting users to the post view after a save event:
#    def change_view(self, request, object_id, extra_context=None, *args, **kwargs):
#        result = super(PostAdmin, self).change_view(request, object_id, extra_context, *args, **kwargs)
#        print type(result), vars(result)

#        post = Post.objects.get(id__exact=object_id)
#
#        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
#            result['Location'] = post.get_absolute_url()
#        return result

    # Custom Admin:
    def my_view(self, request):
        return admin_view(request, self)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        urls = super(PostAdmin, self).get_urls()
        my_urls = patterns('',
               (r'^views/$', self.my_view)
        )
        return my_urls + urls


class CommentAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change, *args, **kwargs):
        if getattr(obj, 'maker', None) is None:
            obj.maker = request.user
            obj.save()

    def queryset(self, request):
        qs = super(CommentAdmin, self).queryset(request)

        # If super-user, show all comment
        if request.user.is_superuser:
            return qs
        return qs.filter(maker=request.user)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
