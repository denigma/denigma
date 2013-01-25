from django.contrib import admin

from models import Entity, Relation


class EntityAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')


class RelationAdmin(admin.ModelAdmin):
    search_fields = ('source', 'type', 'target')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Relation, RelationAdmin)
