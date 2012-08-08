from django.contrib import admin
from polls.models import Poll
from polls.models import Choice


class ChoiceInline(admin.TabularInline): # StackedInline.
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question']
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_today',) #'was_published_recently') # Not available in Django version 1.3.
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierachy = 'pub_date'

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice) # Comment out?
