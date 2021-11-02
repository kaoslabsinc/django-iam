from building_blocks.admin.blocks import HasNameAdminBlock, HasDescriptionAdminBlock
from building_blocks.admin.mixins import EditReadonlyAdminMixin
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdminMixin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(
    EditReadonlyAdminMixin,
    ObjectPermissionsModelAdminMixin,
    admin.ModelAdmin
):
    search_fields = (
        *HasNameAdminBlock.search_fields,
        'author',
    )
    list_display = (
        *HasNameAdminBlock.list_display,
        'author',
    )
    edit_readonly_fields = (
        'author',
    )
    autocomplete_fields = (
        'author',
    )
    fieldsets = (
        (None, {'fields': (
            *HasNameAdminBlock.fields,
            *HasDescriptionAdminBlock.fields,
            'author',
        )}),
    )
