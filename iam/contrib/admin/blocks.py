from building_blocks.admin.blocks import AdminBlock, HasUserAdminBlock, ArchivableAdminBlock
from building_blocks.admin.mixins import EditReadonlyAdminMixin


class ProfileAdminBlock(EditReadonlyAdminMixin, AdminBlock):
    search_fields = HasUserAdminBlock.search_fields
    list_display = (
        *HasUserAdminBlock.list_display,
        *ArchivableAdminBlock.list_display,
    )
    list_filter = ArchivableAdminBlock.list_filter

    readonly_fields = ArchivableAdminBlock.readonly_fields
    edit_readonly_fields = HasUserAdminBlock.edit_readonly_fields
    autocomplete_fields = HasUserAdminBlock.autocomplete_fields
    fieldsets = (
        (None, {'fields': HasUserAdminBlock.fields}),
        *ArchivableAdminBlock.fieldsets,
    )


class HasOwnerAdminBlock(EditReadonlyAdminMixin, AdminBlock):
    search_fields = ('owner__user__username',)
    list_display = ('owner',)
    autocomplete_fields = ('owner',)
    edit_readonly_fields = ('owner',)
    fields = ('owner',)


__all__ = [
    'ProfileAdminBlock',
    'HasOwnerAdminBlock',
]
