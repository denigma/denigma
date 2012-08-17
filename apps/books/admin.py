from django.contrib import admin
from books.models import Publisher, Author, Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'url_link', 'status_link', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'comment')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    fields = ('title', 'comment', 'url', 'status', 'authors', 'publisher') #, 'publication_date'
    filter_horizontal = ('authors',)
##    filter_vertical = ('authors',)
    raw_id_fields = ('publisher',)
    
    def url_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, 'link')
    url_link.allow_tags = True

    def status_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.status, obj.status)
    status_link.allow_tags = True


admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
