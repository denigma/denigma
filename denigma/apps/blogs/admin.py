from django.contrib import admin

from blogs.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Blog, BlogAdmin)

#class EntryAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#admin.site.register(Entry, EntryAdmin)

