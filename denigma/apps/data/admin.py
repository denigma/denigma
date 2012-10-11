from django.contrib import admin

import reversion

from models import Entry, Change, Tag, Relation, Alteration, Category


#class ChangeInline(admin.StackedInline):
#    model = Change
#    fk_name = 'of'
#
#class RelationInline(admin.StackedInline):
#    model = Relation
#    fk_name = 'fr'
#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.request = request
#        obj.save()


class EntryAdmin(reversion.VersionAdmin):
    search_fields = ('title', 'text', 'url')
    order_by =('-created',)
    #inlines = [ChangeInline]
    #inlines = [RelationInline]
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
    order_by  = ('-at',)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Alteration)
admin.site.register(Category)