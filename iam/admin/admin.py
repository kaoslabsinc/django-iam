from building_blocks.admin.admin import ArchivableAdmin
from building_blocks.admin.mixins import EditReadonlyAdminMixin
from django.contrib import admin

from .blocks import ProfileAdminBlock


class ProfileAdmin(
    ArchivableAdmin,
    EditReadonlyAdminMixin,
    admin.ModelAdmin
):
    search_fields = ProfileAdminBlock.search_fields
    list_display = ProfileAdminBlock.list_display
    list_filter = ProfileAdminBlock.list_filter

    readonly_fields = ProfileAdminBlock.readonly_fields
    edit_readonly_fields = ProfileAdminBlock.edit_readonly_fields
    autocomplete_fields = ProfileAdminBlock.autocomplete_fields
    fieldsets = ProfileAdminBlock.fieldsets
