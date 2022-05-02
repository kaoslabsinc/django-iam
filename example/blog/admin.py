from building_blocks.admin import HasNameAdmin, HasDescriptionAdmin
from django.contrib import admin

from iam.contrib.admin import AutoOwnerAdminMixin, HasOwnerAdmin, ObjectPermissionsProfileAdmin
from .models import BlogAdminProfile, BlogAuthorProfile, BlogPost

admin.site.register(BlogAdminProfile, ObjectPermissionsProfileAdmin)
admin.site.register(BlogAuthorProfile, ObjectPermissionsProfileAdmin)


@admin.register(BlogPost)
class BlogPostAdmin(
    HasOwnerAdmin,
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
        *HasDescriptionAdmin.fields,
    )
