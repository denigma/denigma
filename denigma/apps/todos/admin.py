from django.contrib import admin

from models import Todo


class TodoAdmin(admin.ModelAdmin): # Revision  raises error: django.contrib.auth.models.DoesNotExist
    fields = ('title', 'description', 'priority', 'difficulty', 'value', 'start_date', 'stop_date',
              'done', 'creator', 'executor') # 'updated')# 'created',
    list_display = ['title', 'description', 'priority',
                    'start_date', 'stop_date', 'created', 'updated', 'done', 'onhold']
    search_fields = ['title', 'description']
    list_filter  = ('done', 'priority', 'difficulty', 'value', 'created',
                    'updated', 'start_date', 'stop_date', 'done', 'onhold')


admin.site.register(Todo, TodoAdmin)

#234567891123456789212345678931234567894123456789512345678961234567897123456789
