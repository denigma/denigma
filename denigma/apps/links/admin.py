# -*- coding: utf-8 -*-
"""Admin for links."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

import reversion

from models import Category, Link, Country


class LinkAdmin(reversion.VersionAdmin):
    list_display = ('title', 'link', 'description', 'creation', 'visibility', 'site')
    date_hierarchy = 'creation'
    list_filter = ('visibility', 'site', 'creation', 'category')
    search_fields = ('title', 'description', 'url')
    fieldsets = ((None, {'fields': ('title', 'description', 'url')}),
                 (_('Attributes'), {'fields': ('language', 'countries', 'category',)}),
                 (_('Attributes'), {'fields': ('visibility', 'site', 'ordering',
                                               'publication_start', 'publication_end')}),
                 )
    filter_horizontal = ('category', 'countries')
    def link(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, 'link')
    link.allow_tags = True


class CategoryAdmin(reversion.VersionAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    prepropulated_fields = {'slug':('title',)}


admin.site.register(Link, LinkAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country)
    
