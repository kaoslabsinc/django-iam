import pytest

from iam.contrib.perms import Perms


class TestPerms:
    @pytest.fixture
    def user_non_staff(self, create_user):
        return create_user()

    @pytest.fixture
    def user_staff(self, create_user):
        return create_user(is_staff=True)

    def test_all_is_staff(self, user_non_staff, user_staff):
        add_perm = Perms.all_is_staff['add']
        view_perm = Perms.all_is_staff['view']
        change_perm = Perms.all_is_staff['change']
        delete_perm = Perms.all_is_staff['delete']

        assert not add_perm.test(user_non_staff)
        assert not view_perm.test(user_non_staff)
        assert not change_perm.test(user_non_staff)
        assert not delete_perm.test(user_non_staff)

        assert add_perm.test(user_staff)
        assert view_perm.test(user_staff)
        assert change_perm.test(user_staff)
        assert delete_perm.test(user_staff)


    def test_Perms_staff_readonly(self, user_non_staff, user_staff):
        add_perm = Perms.staff_readonly['add']
        view_perm = Perms.staff_readonly['view']
        change_perm = Perms.staff_readonly['change']
        delete_perm = Perms.staff_readonly['delete']

        assert not add_perm.test(user_non_staff)
        assert not view_perm.test(user_non_staff)
        assert not change_perm.test(user_non_staff)
        assert not delete_perm.test(user_non_staff)

        assert not add_perm.test(user_staff)
        assert view_perm.test(user_staff)
        assert not change_perm.test(user_staff)
        assert not delete_perm.test(user_staff)
