from django.contrib import admin

from models import Entity, Relation


class EntityAdmin(admin.ModelAdmin):
    pass

class RelationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Entity, EntityAdmin)
admin.site.register(Relation, RelationAdmin)
