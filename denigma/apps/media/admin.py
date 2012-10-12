from django.contrib import admin

import reversion

from models import Image


class ImageAdmin(reversion.VersionAdmin):
    pass
##    #fields = ['pub_date', 'question']
##    fieldsets = [
##        (None,               {'fields': ['question']}),
##        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
##    ]
##    inlines = [ChoiceInline]
##    list_display = ('question', 'pub_date', 'was_published_today',) #'was_published_recently') # Not available in Django version 1.3.
##    list_filter = ['pub_date']
##    search_fields = ['question']
##    date_hierachy = 'pub_date'


admin.site.register(Image, ImageAdmin)

