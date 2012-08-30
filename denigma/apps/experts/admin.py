from django.contrib import admin

import reversion

from models import *


class DayAdmin(admin.ModelAdmin): #sOfWeek:
    pass


class BusinessHourAdmin(admin.ModelAdmin):
    """Working hours in a business day."""


class WorkingHourAdmin(admin.ModelAdmin):
    """Work."""
##    profile = models.ForeignKey("Profile") #User
##    day = models.ForeignKey("Day")
##    from_time = models.TimeField()
##    to_time = models.TimeField()


class OpeningTimeAdmin(admin.ModelAdmin):
    """The time where an institition is open."""
##    day = models.CharField(max_length=10)
##    start = models.TimeField()
##    end = models.TimeField()


class InstituteAdmin(admin.ModelAdmin):
    """An academic institution such as a university."""
##    name = models.CharField(max_length=250)


class ProfileAdmin(reversion.VersionAdmin): #User
    """The profile of a user."""
    list_display = ('first_name', 'last_name', 'affliation', 'country', 'email', 'link')
    search_fields = ('user_name', 'email',  'affliation', 'work')
    list_filter = ('country',)
    def link(self, obj):
        return '<a href="%s">%s</a>' % (obj.website, obj.website)
    link.allow_tags =True


admin.site.register(Day, DayAdmin)
admin.site.register(BusinessHour, BusinessHourAdmin)
admin.site.register(WorkingHour, WorkingHourAdmin)
admin.site.register(OpeningTime, OpeningTimeAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Profile, ProfileAdmin)

