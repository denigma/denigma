from django.contrib import admin

import reversion

from models import Post


class PostAdmin(reversion.VersionAdmin):
    list_display = ('title', 'brief', 'tagged', 'created', 'updated', 'published')
    list_filter = ['created', 'updated', 'tags__name']
    fields = ('title', 'text', 'tags', 'images', 'published')

    def tagged(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    tagged.allow_tag = True


admin.site.register(Post, PostAdmin)
