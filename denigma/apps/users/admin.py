from django.contrib import admin
from users.models import *

class DayAdmin(admin.ModelAdmin): #sOfWeek:
    pass
admin.site.register(Day, DayAdmin)

class BusinessHourAdmin(admin.ModelAdmin):
    """Working hours in a business day."""
admin.site.register(BusinessHour, BusinessHourAdmin)


class WorkingHourAdmin(admin.ModelAdmin):
    """Work."""
##    profile = models.ForeignKey("Profile") #User
##    day = models.ForeignKey("Day")
##    from_time = models.TimeField()
##    to_time = models.TimeField()
admin.site.register(WorkingHour, WorkingHourAdmin)


class OpeningTimeAdmin(admin.ModelAdmin):
    """The time where an institition is open."""
##    day = models.CharField(max_length=10)
##    start = models.TimeField()
##    end = models.TimeField()
admin.site.register(OpeningTime, OpeningTimeAdmin)


class InstituteAdmin(admin.ModelAdmin):
    """An academic institution such as a university."""
##    name = models.CharField(max_length=250)
admin.site.register(Institute, InstituteAdmin)


class ProfileAdmin(admin.ModelAdmin): #User
    """The profile of a user."""
    list_display = ('first_name', 'last_name', 'affliation', 'country', 'email', 'link')
    search_fields = ('user_name', 'email',  'affliation', 'work')
    list_filter = ('country',)
    def link(self, obj):
        return '<a href="%s">%s</a>' % (obj.website, obj.website)
    link.allow_tags =True
admin.site.register(Profile, ProfileAdmin)

