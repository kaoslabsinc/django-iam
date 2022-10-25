from building_blocks.admin import ArchivableAdmin, BaseArchivableAdmin
from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin

USER = 'user'


class BaseProfileAdmin(
    BaseArchivableAdmin,
    EditReadonlyAdminMixin,
    BaseModelAdmin
):
    readonly_fields = ArchivableAdmin.readonly_fields
    edit_readonly_fields = (USER,)
    autocomplete_fields = (USER,)
    fields = None
    fieldsets = (
        (None, {'fields': (USER,)}),
        *ArchivableAdmin.fieldsets,
    )


class BaseProfileInlineAdmin(
    BaseProfileAdmin,
    InlineModelAdmin
):
    extra = 0
    show_change_link = True


class BaseProfileModelAdmin(
    ArchivableAdmin,
    BaseProfileAdmin,
    admin.ModelAdmin
):
    """
    Base admin class for profile models.
    """
    search_fields = ('user__username',)
    list_display = (
        USER,
        *ArchivableAdmin.list_display,
    )
    list_filter = ArchivableAdmin.list_filter

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
    'BaseProfileInlineAdmin',
    'BaseProfileModelAdmin',
    'ProfileAdmin',
)
