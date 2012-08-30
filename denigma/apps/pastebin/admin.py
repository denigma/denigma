from django.contrib import admin

import reversion

from models import PastedItem


class PastedItemAdmin(reversion.VersionAdmin):
    list_display = ('uuid', 'user', 'pasted_at',)
    fields = ('text', 'in_response_to', 'user',)


admin.site.register(PastedItem, PastedItemAdmin)
