from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin


class HasOwnerAdmin(EditReadonlyAdminMixin, admin.ModelAdmin):
    search_fields = ('owner__user__username',)
    list_display = ('owner_display',)
    autocomplete_fields = ('owner',)
    edit_readonly_fields = ('owner',)
    fields = ('owner',)

    @admin.display(ordering='owner')
    def owner_display(self, obj):
        return obj and obj.owner.user
