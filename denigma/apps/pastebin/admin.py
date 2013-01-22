from django.contrib import admin

import reversion

from models import PastedItem


class PastedItemAdmin(reversion.VersionAdmin):
    list_display = ('uuid', 'short', 'user', 'pasted_at')
    fields = ('text', 'in_response_to', 'user')
    list_filter = ('user', 'pasted_at')
    search_fields = ('text',)


admin.site.register(PastedItem, PastedItemAdmin)
