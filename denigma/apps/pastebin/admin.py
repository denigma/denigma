from django.contrib import admin
from models import PastedItem

class PastedItemAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'pasted_at',)
    fields = ('text', 'in_response_to', 'user',)

admin.site.register(PastedItem, PastedItemAdmin)

