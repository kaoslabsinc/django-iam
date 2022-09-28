from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin


class HasOwnerAdmin(EditReadonlyAdminMixin, admin.ModelAdmin):
    """
    Admin class for models that have an owner relational field to a profile model.
    Use as a base for your admin classes or use its static fields (e.g. `search_fields` or `list_display`) for a
    standardized admin interface for models with an owner.
    """
    search_fields = ('owner__user__username',)
    list_display = ('owner_display',)
    autocomplete_fields = ('owner',)
    edit_readonly_fields = ('owner',)
    fields = ('owner',)

    @admin.display(ordering='owner')
    def owner_display(self, obj):
        return obj and obj.owner.user
