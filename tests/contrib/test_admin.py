from building_blocks.consts.field_names import OWNER

from iam.contrib.admin import HasOwnerAdminBlock, HasAuthorAdminBlock


def test_HasOwnerAdminBlock():
    assert HasOwnerAdminBlock.autocomplete_fields == (OWNER,)
    assert HasOwnerAdminBlock.base_fields == (OWNER,)
    assert HasOwnerAdminBlock.edit_readonly_fields == (OWNER,)
    assert HasOwnerAdminBlock.list_display == ('owner_display',)
    assert HasOwnerAdminBlock.owner_field == OWNER
    assert HasOwnerAdminBlock.search_fields == ('owner__user__username',)


def test_HasAuthorAdminBlock():
    assert HasAuthorAdminBlock.autocomplete_fields == ('author',)
    assert HasAuthorAdminBlock.base_fields == ('author',)
    assert HasAuthorAdminBlock.edit_readonly_fields == ('author',)
    assert HasAuthorAdminBlock.list_display == ('author_display',)
    assert HasAuthorAdminBlock.owner_field == 'author'
    assert HasAuthorAdminBlock.search_fields == ('author__user__username',)
