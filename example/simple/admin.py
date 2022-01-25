from building_blocks.admin import HasNameAdmin
from django.contrib import admin

from iam.contrib.admin import AutoOwnerAdminMixin, HasOwnerAdmin, ObjectPermissionsProfileAdmin
from .models import SimpleAdminProfile, SimpleObject

admin.site.register(SimpleAdminProfile, ObjectPermissionsProfileAdmin)


@admin.register(SimpleObject)
class SimpleObjectAdmin(
    AutoOwnerAdminMixin,
    admin.ModelAdmin
):
    search_fields = (
        *HasNameAdmin.search_fields,
        *HasOwnerAdmin.search_fields
    )
    list_display = (
        *HasNameAdmin.list_display,
        *HasOwnerAdmin.list_display
    )
    autocomplete_fields = HasOwnerAdmin.autocomplete_fields
    edit_readonly_fields = HasOwnerAdmin.edit_readonly_fields
    fields = (
        *HasNameAdmin.fields,
        *HasOwnerAdmin.fields,
    )
