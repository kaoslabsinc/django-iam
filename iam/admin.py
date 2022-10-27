from building_blocks.consts.field_names import *
from building_blocks.models.admin import BaseArchivableAdminMixin, ArchivableAdminBlock, ArchivableAdminMixin
from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin


class ProfileAdminBlock(ArchivableAdminBlock):
    edit_readonly_fields = (USER,)
    autocomplete_fields = (USER,)
    the_fieldset = (None, {'fields': (USER,)})
    list_display = (
        USER,
        *ArchivableAdminBlock.list_display,
    )
    search_fields = ('user__username',)


class BaseProfileAdmin(
    BaseArchivableAdminMixin,
    EditReadonlyAdminMixin,
    BaseModelAdmin
):
    readonly_fields = ProfileAdminBlock.readonly_fields
    edit_readonly_fields = ProfileAdminBlock.edit_readonly_fields
    autocomplete_fields = ProfileAdminBlock.autocomplete_fields
    fieldsets = (
        ProfileAdminBlock.the_fieldset,
        ProfileAdminBlock.the_admin_fieldset,
    )


class BaseProfileInlineAdmin(
    BaseProfileAdmin,
    InlineModelAdmin
):
    extra = 0
    show_change_link = True


class BaseProfileModelAdmin(
    ArchivableAdminMixin,
    BaseProfileAdmin,
    admin.ModelAdmin
):
    """
    Base admin class for profile models.
    """
    search_fields = ProfileAdminBlock.search_fields
    list_display = ProfileAdminBlock.list_display
    list_filter = ProfileAdminBlock.list_filter

    @admin.action(permissions=['change'], description="Deactivate")
    def archive(self, request, queryset):  # Overridden here to change the label (^ description="Deactivate")
        return super(BaseProfileModelAdmin, self).archive(request, queryset)

    archive.label = "Deactivate"


class ProfileAdmin(
    ObjectPermissionsModelAdminMixin,
    BaseProfileModelAdmin
):
    """
    Admin class for profile models that comes with `ObjectPermissionsModelAdminMixin`. In most cases you should use
    this class over `BaseProfileAdmin`.
    """
    pass


__all__ = (
    'ProfileAdminBlock',
    'BaseProfileInlineAdmin',
    'BaseProfileModelAdmin',
    'ProfileAdmin',
)
