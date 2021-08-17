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
    edit_readonly_fields = (*HasUserAdminBlock.edit_readonly_fields,)
    autocomplete_fields = HasUserAdminBlock.autocomplete_fields
    fieldsets = (
        *HasUserAdminBlock.fieldsets,
        *ArchivableAdminBlock.fieldsets,
    )
