import pytest
from django.utils.translation import gettext_lazy as _

from iam.contrib.users.admin import HideSuperuserUserAdminMixin, BaseIAMUserAdmin, IAMUserAdmin


class TestAbstractIAMUser:
    @pytest.fixture
    def user(self, create_user):
        return create_user(first_name="John", last_name="Smith", username="jsmith")

    @pytest.fixture
    def user_no_name(self, create_user):
        return create_user(username="jsmith2")

    def test_full_name(self, user, user_no_name):
        assert user.full_name == "John Smith"
        assert user_no_name.full_name == ""

    def test_display_name(self, user, user_no_name):
        assert user.display_name == "John Smith"
        assert user_no_name.display_name == "jsmith2"

    def test_display_id(self, user, user_no_name):
        assert user.display_id == "jsmith"
        assert user_no_name.display_id == "jsmith2"


class TestHideSuperuserUserAdminMixin:
    def test_fields(self):
        assert HideSuperuserUserAdminMixin.exclude_from_non_superusers == ('is_superuser', 'user_permissions')


class TestBaseIAMUserAdmin:
    def test_fields(self):
        assert BaseIAMUserAdmin.add_fieldsets == (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            }),
            (_('Permissions'), {
                'classes': ('wide',),
                'fields': ('is_staff',),
            }),
            (_('Personal info'), {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name',),
            }),
        )
        assert BaseIAMUserAdmin.list_display == ('username', 'email', 'full_name', 'is_active', 'is_staff')
        assert BaseIAMUserAdmin.search_fields == ('username', 'email', 'first_name', 'last_name')
        assert BaseIAMUserAdmin.list_filter == ('is_staff', 'is_active', 'groups')
        assert BaseIAMUserAdmin.readonly_fields == ('date_joined', 'last_login',)


class TestIAMUserAdmin:
    def test_fields(self):
        assert IAMUserAdmin.add_fieldsets == BaseIAMUserAdmin.add_fieldsets
        assert IAMUserAdmin.list_display == BaseIAMUserAdmin.list_display
        assert IAMUserAdmin.search_fields == BaseIAMUserAdmin.search_fields
        assert IAMUserAdmin.list_filter == BaseIAMUserAdmin.list_filter
        assert IAMUserAdmin.readonly_fields == BaseIAMUserAdmin.readonly_fields
