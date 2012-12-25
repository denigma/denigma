from django.contrib import admin

from models import Visitor, BannedIP, UntrackedUserAgent, Activity


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user', 'location', 'activities', 'session_start', 'last_update', 'time_on_site', 'inactive_time') #'country',
    ordering = ('-last_update',)
    readonly_fields = ('country',)

    def location(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)

    location.allow_tags = True

    def activities(self, obj):
        return '<a href="/admin/track/activity/?visitor__id__exact=%s">%s</a>' % (obj.pk, obj.page_views)
    activities.allow_tags = True

    #def country(self, obj):
        #print obj.country
       # return obj.country
    #    return locate(obj.ip_address)
    #country.allow_tags = True

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'link', 'url', 'view_time')
    ordering = ('-id',)
    #list_filter = ('visitor', 'url')

    def link(self, obj):
        return '<a href="/admin/track/activity/%s/">%s</a>' % (obj.visitor.pk, obj.visitor.user_agent)
    link.allow_tags = True


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)
admin.site.register(Activity, ActivityAdmin)