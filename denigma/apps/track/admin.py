from django.contrib import admin

from models import Visitor, BannedIP, UntrackedUserAgent


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user', 'location', 'page_views', 'session_start', 'last_update')

    def location(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)

    location.allow_tags = True

admin.site.register(Visitor, VisitorAdmin)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)