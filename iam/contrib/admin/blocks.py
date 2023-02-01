from building_blocks.admin import BaseAdminBlock
from building_blocks.consts.field_names import *
from dj_kaos_utils.admin import EditReadonlyAdminMixin
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin


# TODO: deprecate .author in favor of sole .owner

def _get_owner_cls_name_fragment(owner_field):
    return owner_field.replace('_', ' ').title().replace(' ', '')


def _get_owner_display_label(owner_field):
    return owner_field.replace('_', ' ')


def has_owner_admin_block_factory(_owner_field=OWNER):
    class HasXXXAdminBlock(BaseAdminBlock):
        owner_field = _owner_field
        search_fields = (f'{owner_field}__{USER}__username',)
        list_display = (f'{owner_field}_display',)
        autocomplete_fields = (owner_field,)
        edit_readonly_fields = (owner_field,)
        base_fields = (owner_field,)

    owner_cls_name_fragment = _get_owner_cls_name_fragment(_owner_field)
    HasXXXAdminBlock.__name__ = HasXXXAdminBlock.__name__.replace('XXX', owner_cls_name_fragment)
    return HasXXXAdminBlock


HasOwnerAdminBlock = has_owner_admin_block_factory()
"""Admin block for models with an owner linked to a profile"""
HasAuthorAdminBlock = has_owner_admin_block_factory(AUTHOR)
"""Admin block for models with an author linked to a profile"""


def base_has_owner_admin_mixin_factory(admin_block_cls=HasOwnerAdminBlock):
    owner_field = admin_block_cls.owner_field

    class BaseHasXXXAdminMixin(EditReadonlyAdminMixin, BaseModelAdmin):
        autocomplete_fields = admin_block_cls.autocomplete_fields
        edit_readonly_fields = admin_block_cls.edit_readonly_fields

        @admin.display(
            description=_get_owner_display_label(owner_field),
            ordering=owner_field
        )
        def owner_display(self, obj):
            return obj and getattr(obj, owner_field).user

    owner_cls_name_fragment = _get_owner_cls_name_fragment(owner_field)
    BaseHasXXXAdminMixin.__name__ = BaseHasXXXAdminMixin.__name__.replace('XXX', owner_cls_name_fragment)
    return BaseHasXXXAdminMixin


BaseHasOwnerAdminMixin = base_has_owner_admin_mixin_factory()
BaseHasAuthorAdminMixin = base_has_owner_admin_mixin_factory(HasAuthorAdminBlock)


def has_owner_admin_mixin_factory(admin_block_cls=HasOwnerAdminBlock):
    class HasXXXAdminMixin(EditReadonlyAdminMixin, BaseModelAdmin):
        search_fields = admin_block_cls.search_fields
        list_display = admin_block_cls.list_display

    owner_cls_name_fragment = _get_owner_cls_name_fragment(admin_block_cls.owner_field)
    HasXXXAdminMixin.__name__ = HasXXXAdminMixin.__name__.replace('XXX', owner_cls_name_fragment)
    return HasXXXAdminMixin


HasOwnerAdminMixin = has_owner_admin_mixin_factory()
HasAuthorAdminMixin = has_owner_admin_mixin_factory(HasAuthorAdminBlock)

__all__ = (
    'has_owner_admin_block_factory',
    'base_has_owner_admin_mixin_factory',
    'has_owner_admin_mixin_factory',
    'HasOwnerAdminBlock',
    'HasAuthorAdminBlock',
    'BaseHasOwnerAdminMixin',
    'BaseHasAuthorAdminMixin',
    'HasOwnerAdminMixin',
    'HasAuthorAdminMixin',
)
