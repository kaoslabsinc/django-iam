from building_blocks.admin import ArchivableAdmin
from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin


class BaseProfileAdmin(
    ArchivableAdmin,
    EditReadonlyAdminMixin,
    admin.ModelAdmin
):
    """
    Base admin class for profile models.
    """
    USER = 'user'

    search_fields = ('user__username',)
    list_display = (
        USER,
        ArchivableAdmin.list_display,
    )
    list_filter = ArchivableAdmin.list_filter

    readonly_fields = ArchivableAdmin.readonly_fields
    edit_readonly_fields = (USER,)
    autocomplete_fields = (USER,)
    fields = None
    fieldsets = (
        (None, {'fields': (USER,)}),
        *ArchivableAdmin.fieldsets,
    )

    @admin.action(permissions=['change'], description="Deactivate")
    def archive(self, request, queryset):  # Overridden here to change the label (^ description="Deactivate")
        return super(BaseProfileAdmin, self).archive(request, queryset)

    archive.label = "Deactivate"


class ProfileAdmin(
    ObjectPermissionsModelAdminMixin,
    BaseProfileAdmin
):
    """
    Admin class for profile models that comes with `ObjectPermissionsModelAdminMixin`. In most cases you should use
    this class over `BaseProfileAdmin`.
    """
    pass


class HasOwnerAdmin(EditReadonlyAdminMixin, admin.ModelAdmin):
    search_fields = ('owner__user__username',)
    list_display = ('owner_display',)
    autocomplete_fields = ('owner',)
    edit_readonly_fields = ('owner',)
    fields = ('owner',)

    @admin.display(ordering='owner')
    def owner_display(self, obj):
        return obj and obj.owner.user


__all__ = [
    'BaseProfileAdmin',
    'ProfileAdmin',
    'HasOwnerAdmin',
]
