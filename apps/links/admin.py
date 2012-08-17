# -*- coding: utf-8 -*-
"""Admin for links."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from links.models import Category
from links.models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'description', 'language', 'visibility', 'site')
    date_hierarchy = 'creation'
    list_filter = ('visibility', 'site', 'creation', 'category')
    search_fields = ('title', 'description', 'url')
    fieldsets = ((None, {'fields': ('title', 'description', 'url')}),
                 (_('Attributes'), {'fields': ('language', 'category',)}),
                 (_('Attributes'), {'fields': ('visibility', 'site', 'ordering',
                                               'publication_start', 'publication_end')}),
                 )
    filter_horizontal = ('category',)
    def link(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, 'link')
    link.allow_tags = True
        

admin.site.register(Link, LinkAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    prepropulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)
    
