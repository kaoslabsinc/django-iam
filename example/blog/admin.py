from building_blocks.admin.blocks import HasNameAdminBlock, HasDescriptionAdminBlock
from building_blocks.admin.mixins import EditReadonlyAdminMixin
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin

from iam.admin.admin import ObjectPermissionsProfileAdmin
from iam.admin.blocks import HasOwnerAdminBlock
from .models import BlogManager, BlogAuthor, BlogPost

admin.site.register(BlogManager, ObjectPermissionsProfileAdmin)
admin.site.register(BlogAuthor, ObjectPermissionsProfileAdmin)


@admin.register(BlogPost)
class BlogPostAdmin(
    EditReadonlyAdminMixin,
    ObjectPermissionsModelAdminMixin,
    admin.ModelAdmin
):
    search_fields = (
        *HasNameAdminBlock.search_fields,
        *HasOwnerAdminBlock.search_fields,
    )
    list_display = (
        *HasNameAdminBlock.list_display,
        *HasOwnerAdminBlock.list_display,
    )
    edit_readonly_fields = (
        *HasOwnerAdminBlock.edit_readonly_fields,
    )
    autocomplete_fields = (
        *HasOwnerAdminBlock.autocomplete_fields,
    )
    fieldsets = (
        (None, {'fields': (
            *HasNameAdminBlock.fields,
            *HasDescriptionAdminBlock.fields,
            *HasOwnerAdminBlock.fields,
        )}),
    )
