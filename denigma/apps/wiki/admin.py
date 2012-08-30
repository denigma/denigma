from django.contrib import admin

import reversion

from models import Page, Tag


class PageAdmin(reversion.VersionAdmin):
   list_display = ('name', 'tagged',)
   list_filter = ('tags',)

   def tagged(self, obj):
       return " ".join([tag.name for tag in obj.tags.all()])
   tagged.allow_tags = True


class TagAdmin(reversion.VersionAdmin):
   list_display = ('name', 'pages',)

   def pages(self, obj):
       print obj.page_set.all()
       return " ".join(page.name for page in obj.page_set.all())
   pages.allow_tags = True


admin.site.register(Tag, TagAdmin)
admin.site.register(Page, PageAdmin)

