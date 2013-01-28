from django.contrib import admin

from models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('time', 'server', 'channel', 'nickname', 'short')
    list_filter = ('server', 'channel', 'nickname')
    search_fields = ('channel', 'nickname', 'message')
    date_hierarchy = 'time'


admin.site.register(Message, MessageAdmin)