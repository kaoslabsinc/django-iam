from building_blocks.admin.blocks import HasNameAdminBlock
from django.contrib import admin

from iam.contrib.admin import AutoOwnerAdminMixin, HasOwnerAdminBlock, ObjectPermissionsProfileAdmin
from .models import SimpleAdminProfile, SimpleObject

admin.site.register(SimpleAdminProfile, ObjectPermissionsProfileAdmin)


@admin.register(SimpleObject)
class SimpleObjectAdmin(
    AutoOwnerAdminMixin,
    admin.ModelAdmin
):
    search_fields = (
        *HasNameAdminBlock.search_fields,
        *HasOwnerAdminBlock.search_fields
    )
    list_display = (
        *HasNameAdminBlock.list_display,
        *HasOwnerAdminBlock.list_display
    )
    autocomplete_fields = HasOwnerAdminBlock.autocomplete_fields
    edit_readonly_fields = HasOwnerAdminBlock.edit_readonly_fields
    fields = (
        *HasNameAdminBlock.fields,
        *HasOwnerAdminBlock.fields,
    )
