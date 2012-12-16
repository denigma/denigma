from django.contrib import admin

from models import Visitor, BannedIP, UntrackedUserAgent


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user', 'url', 'page_views', 'session_start', 'last_update')


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)