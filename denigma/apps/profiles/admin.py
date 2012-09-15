from django.contrib import admin

from profiles.models import Profile, Rank, Grade, Title, Role


admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Grade)
admin.site.register(Title)
admin.site.register(Role)
