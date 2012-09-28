from django.contrib import admin

from models import Profile, Rank, Grade, Title, Role


class RoleAdmin(admin.ModelAdmin):
    fields = ('name', 'description')

admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Grade)
admin.site.register(Title)
admin.site.register(Role)
