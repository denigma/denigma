from django.contrib import admin

import reversion

from models import Entry, Change, Tag, Relation, Alteration


class EntryAdmin(reversion.VersionAdmin):
    def save_model(self, request, obj, form, change):
        print("EntryAdmin.save_model here!")
        obj.user = request.user
        obj.request = request
        obj.save()


class RelationAdmin(reversion.VersionAdmin):
    def save_model(self, request, obj, form, change):
        print("RelationAdmin.save_model here!")
        obj.user = request.user
        obj.save()


class TagAdmin(reversion.VersionAdmin):
    pass


class ChangeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')


admin.site.register(Entry, EntryAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Alteration)