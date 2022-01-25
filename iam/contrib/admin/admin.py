from building_blocks.admin import HasUserAdmin
from building_blocks.admin.admin import ArchivableAdmin
from building_blocks.admin.mixins import EditReadonlyAdminMixin
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin


class ProfileAdmin(
    ArchivableAdmin,
    EditReadonlyAdminMixin,
    admin.ModelAdmin
):
    search_fields = HasUserAdmin.search_fields
    list_display = (
        *HasUserAdmin.list_display,
        *ArchivableAdmin.list_display,
    )
    list_filter = ArchivableAdmin.list_filter

    readonly_fields = ArchivableAdmin.readonly_fields
    edit_readonly_fields = HasUserAdmin.edit_readonly_fields
    autocomplete_fields = HasUserAdmin.autocomplete_fields
    fields = None
    fieldsets = (
        (None, {'fields': HasUserAdmin.fields}),
        *ArchivableAdmin.fieldsets,
    )

    @admin.action(permissions=['change'], description="Deactivate")
    def archive(self, request, queryset):
        return super(ProfileAdmin, self).archive(request, queryset)

    archive.label = "Deactivate"


class ObjectPermissionsProfileAdmin(
    ObjectPermissionsModelAdminMixin,
    ProfileAdmin
):
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
    'ProfileAdmin',
    'ObjectPermissionsProfileAdmin',
    'HasOwnerAdmin',
]
