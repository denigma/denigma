from django.contrib import admin
from models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'brief', 'tagged', 'created', 'updated')
    list_filter = ['created', 'updated', 'tags__name']

    def tagged(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tagged.allow_tag = True

admin.site.register(Post, PostAdmin)
