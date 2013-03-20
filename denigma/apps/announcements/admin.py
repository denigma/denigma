from django.contrib import admin

from models import Announcement, Dismissal
from forms import AnnouncementAdminForm



class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "creator","creation_date", "members_only")
    list_filter = ("members_only",)
    form = AnnouncementAdminForm
    fieldsets = [
        (None, {
            "fields": ["title", "content", "site_wide", "members_only", "publish_start", "publish_end", "dismissal_type"],
            }),
        ("Manage announcement", {
            "fields": ["users", "send_now"]

        }),
    ]
    #filter_horizontal = ('user',)

    def save_model(self, request, obj, form, change):
        if not change:
            # When creating a new announcement, set the creator field.
            obj.creator = request.user
        obj.save()


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Dismissal)