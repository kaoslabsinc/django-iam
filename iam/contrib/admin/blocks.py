from building_blocks.consts.field_names import *
from building_blocks.models.admin import BaseAdminBlock
from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin


class HasOwnerAdminBlock(BaseAdminBlock):
    search_fields = (f'{OWNER}__{USER}__username',)
    list_display = (f'{OWNER}_display',)
    autocomplete_fields = (OWNER,)
    edit_readonly_fields = (OWNER,)
    base_fields = (OWNER,)


class BaseHasOwnerAdminMixin(EditReadonlyAdminMixin, BaseModelAdmin):
    autocomplete_fields = HasOwnerAdminBlock.autocomplete_fields
    edit_readonly_fields = HasOwnerAdminBlock.edit_readonly_fields

    @admin.display(description="owner", ordering=OWNER)
    def owner_display(self, obj):
        return obj and obj.owner.user


class HasOwnerAdminMixin(BaseHasOwnerAdminMixin, admin.ModelAdmin):
    """
    Admin class for models that have an owner relational field to a profile model.
    Use as a base for your admin classes or use its static fields (e.g. `search_fields` or `list_display`) for a
    standardized admin interface for models with an owner.
    """
    search_fields = HasOwnerAdminBlock.search_fields
    list_display = HasOwnerAdminBlock.list_display


class HasAuthorAdminBlock(BaseAdminBlock):
    search_fields = (f'{AUTHOR}__{USER}__username',)
    list_display = (f'{AUTHOR}_display',)
    autocomplete_fields = (AUTHOR,)
    edit_readonly_fields = (AUTHOR,)
    base_fields = (AUTHOR,)


class BaseHasAuthorAdminMixin(EditReadonlyAdminMixin, BaseModelAdmin):
    autocomplete_fields = HasAuthorAdminBlock.autocomplete_fields
    edit_readonly_fields = HasAuthorAdminBlock.edit_readonly_fields

    @admin.display(description="author", ordering=AUTHOR)
    def author_display(self, obj):
        return obj and obj.author.user


class HasAuthorAdminMixin(BaseHasAuthorAdminMixin, admin.ModelAdmin):
    """
    Admin class for models that have an author relational field to a profile model.
    Use as a base for your admin classes or use its static fields (e.g. `search_fields` or `list_display`) for a
    standardized admin interface for models with an author.
    """
    search_fields = HasAuthorAdminBlock.search_fields
    list_display = HasAuthorAdminBlock.list_display
