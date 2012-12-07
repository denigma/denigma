from django.contrib import admin

from models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('label', 'done')
    list_filter = ('done',)


admin.site.register(Task, TaskAdmin)