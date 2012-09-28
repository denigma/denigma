from django.contrib import admin
from models import Hierarchy, HierarchyType, Rank, Grade, Title, Role, Language


class HierarchyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'requirement')



class HierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'requirement')
    list_filter = ('type',)

admin.site.register(Hierarchy, HierarchyAdmin)
admin.site.register(HierarchyType, HierarchyTypeAdmin)
admin.site.register(Rank)
admin.site.register(Grade)
admin.site.register(Title)
admin.site.register(Role)
admin.site.register(Language)