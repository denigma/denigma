from django.contrib import admin

import reversion

from models import Todo


class TodoAdmin(reversion.VersionAdmin):
    fields = ('title', 'description', 'importance', 'start_date', 'stop_date',
              'done', 'owner') # 'updated')# 'created',
    list_display = ['title', 'description', 'importance',
                    'start_date', 'stop_date', 'created', 'updated', 'done']
    search_fields = ['title', 'description']
    list_filter  = ('done', 'importance',)


admin.site.register(Todo, TodoAdmin)

#234567891123456789212345678931234567894123456789512345678961234567897123456789
