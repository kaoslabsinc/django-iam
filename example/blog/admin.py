from building_blocks.admin.blocks import HasNameAdminBlock, HasDescriptionAdminBlock
from django.contrib import admin

from iam.contrib.admin.admin import ObjectPermissionsProfileAdmin
from iam.contrib.admin.blocks import HasOwnerAdminBlock
from iam.contrib.admin.mixins import AutoOwnerAdminMixin
from .models import BlogAdminProfile, BlogAuthorProfile, BlogPost

admin.site.register(BlogAdminProfile, ObjectPermissionsProfileAdmin)
admin.site.register(BlogAuthorProfile, ObjectPermissionsProfileAdmin)


@admin.register(BlogPost)
class BlogPostAdmin(
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
        *HasDescriptionAdminBlock.fields,
    )
