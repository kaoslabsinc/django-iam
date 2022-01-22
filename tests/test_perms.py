import pytest
import rules
from django.contrib.auth import get_user_model

from blog.models import BlogPost, BlogAdminProfile, BlogAuthorProfile
from iam.utils import override_perms
from users.models import AppAdminProfile

User = get_user_model()


def has_perm(model_cls, perm, user, obj=None):
    perm = model_cls.get_perm(perm)
    return user.has_perm(perm, obj) if obj else user.has_perm(perm)


class TestPerms:
    @pytest.fixture
    def user_generic(self, django_user_model):
        return django_user_model.objects.create(username='user_generic')

    @pytest.fixture
    def user_staff(self, django_user_model):
        return django_user_model.objects.create(username='user_staff', is_staff=True)

    @pytest.fixture
    def user_blog_author_nonowner(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_author_nonowner', is_staff=True)
        BlogAuthorProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_blog_author_owner(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_author_owner', is_staff=True)
        BlogAuthorProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_blog_admin(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_admin', is_staff=True)
        BlogAdminProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_app_admin(self, django_user_model):
        user = django_user_model.objects.create(username='user_app_admin', is_staff=True)
        AppAdminProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def owner_profile(self, user_blog_author_owner):
        return BlogAuthorProfile.objects.get(user=user_blog_author_owner)

    @pytest.fixture
    def obj(self, owner_profile):
        return BlogPost.objects.get_or_create(name="sss", owner=owner_profile)[0]

    def test_user_generic(self, user_generic, obj):
        assert not has_perm(BlogPost, 'add', user_generic)
        assert not has_perm(BlogPost, 'view', user_generic)
        assert not has_perm(BlogPost, 'view', user_generic, obj)
        assert not has_perm(BlogPost, 'change', user_generic, obj)
        assert not has_perm(BlogPost, 'change', user_generic, obj)
        assert not has_perm(BlogPost, 'delete', user_generic, obj)
        assert not has_perm(BlogPost, 'delete', user_generic, obj)

    def test_user_staff(self, user_staff, obj):
        assert not has_perm(BlogPost, 'add', user_staff)
        assert not has_perm(BlogPost, 'view', user_staff)
        assert not has_perm(BlogPost, 'view', user_staff, obj)
        assert not has_perm(BlogPost, 'change', user_staff)
        assert not has_perm(BlogPost, 'change', user_staff, obj)
        assert not has_perm(BlogPost, 'delete', user_staff)
        assert not has_perm(BlogPost, 'delete', user_staff, obj)

    def test_user_blog_author_nonowner(self, user_blog_author_nonowner, obj):
        assert has_perm(BlogPost, 'add', user_blog_author_nonowner)
        assert has_perm(BlogPost, 'view', user_blog_author_nonowner)
        assert has_perm(BlogPost, 'view', user_blog_author_nonowner, obj)
        assert has_perm(BlogPost, 'change', user_blog_author_nonowner)
        assert not has_perm(BlogPost, 'change', user_blog_author_nonowner, obj)
        assert has_perm(BlogPost, 'delete', user_blog_author_nonowner)
        assert not has_perm(BlogPost, 'delete', user_blog_author_nonowner, obj)

    def test_user_blog_author_owner(self, user_blog_author_owner, obj):
        assert has_perm(BlogPost, 'add', user_blog_author_owner)
        assert has_perm(BlogPost, 'view', user_blog_author_owner)
        assert has_perm(BlogPost, 'view', user_blog_author_owner, obj)
        assert has_perm(BlogPost, 'change', user_blog_author_owner)
        assert has_perm(BlogPost, 'change', user_blog_author_owner, obj)
        assert has_perm(BlogPost, 'delete', user_blog_author_owner)
        assert has_perm(BlogPost, 'delete', user_blog_author_owner, obj)

    def test_user_blog_admin(self, user_blog_admin, obj):
        assert has_perm(BlogPost, 'add', user_blog_admin)
        assert has_perm(BlogPost, 'view', user_blog_admin)
        assert has_perm(BlogPost, 'view', user_blog_admin, obj)
        assert has_perm(BlogPost, 'change', user_blog_admin)
        assert has_perm(BlogPost, 'change', user_blog_admin, obj)
        assert has_perm(BlogPost, 'delete', user_blog_admin)
        assert has_perm(BlogPost, 'delete', user_blog_admin, obj)

    def test_user_app_admin(self, user_app_admin, obj):
        assert has_perm(BlogPost, 'add', user_app_admin)
        assert has_perm(BlogPost, 'view', user_app_admin)
        assert has_perm(BlogPost, 'view', user_app_admin, obj)
        assert has_perm(BlogPost, 'change', user_app_admin)
        assert has_perm(BlogPost, 'change', user_app_admin, obj)
        assert has_perm(BlogPost, 'delete', user_app_admin)
        assert has_perm(BlogPost, 'delete', user_app_admin, obj)

    def test_user_app_admin_deactivated(self, user_app_admin, obj):
        profile = AppAdminProfile.objects.get(user=user_app_admin)
        profile.deactivate()
        profile.save()
        assert not has_perm(BlogPost, 'add', user_app_admin)
        assert not has_perm(BlogPost, 'view', user_app_admin)
        assert not has_perm(BlogPost, 'view', user_app_admin, obj)
        assert not has_perm(BlogPost, 'change', user_app_admin)
        assert not has_perm(BlogPost, 'change', user_app_admin, obj)
        assert not has_perm(BlogPost, 'delete', user_app_admin)
        assert not has_perm(BlogPost, 'delete', user_app_admin, obj)

    def test_override(self, user_generic, obj):
        override_perms(BlogPost, {
            'add': rules.always_allow,
            'view': rules.always_allow,
            'change': rules.always_allow,
            'delete': rules.always_allow,
        })
        assert has_perm(BlogPost, 'add', user_generic)
        assert has_perm(BlogPost, 'view', user_generic)
        assert has_perm(BlogPost, 'view', user_generic, obj)
        assert has_perm(BlogPost, 'change', user_generic, obj)
        assert has_perm(BlogPost, 'change', user_generic, obj)
        assert has_perm(BlogPost, 'delete', user_generic, obj)
        assert has_perm(BlogPost, 'delete', user_generic, obj)


class TestAdminRolePerms:
    @pytest.fixture
    def user_generic(self, django_user_model):
        return django_user_model.objects.create(username='user_generic')

    @pytest.fixture
    def user_staff(self, django_user_model):
        return django_user_model.objects.create(username='user_staff', is_staff=True)

    @pytest.fixture
    def user_blog_author(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_author', is_staff=True)
        BlogAuthorProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_blog_admin(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_admin', is_staff=True)
        BlogAdminProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_app_admin(self, django_user_model):
        user = django_user_model.objects.create(username='user_app_admin', is_staff=True)
        AppAdminProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def obj(self, django_user_model):
        return django_user_model.objects.create(username='some_user')

    def test_user_generic(self, user_generic, obj):
        assert not has_perm(User, 'add', user_generic)
        assert not has_perm(User, 'view', user_generic)
        assert not has_perm(User, 'view', user_generic, obj)
        assert not has_perm(User, 'change', user_generic, obj)
        assert not has_perm(User, 'change', user_generic, obj)
        assert not has_perm(User, 'delete', user_generic, obj)
        assert not has_perm(User, 'delete', user_generic, obj)

    def test_user_staff(self, user_staff, obj):
        assert not has_perm(User, 'add', user_staff)
        assert not has_perm(User, 'view', user_staff)
        assert not has_perm(User, 'view', user_staff, obj)
        assert not has_perm(User, 'change', user_staff)
        assert not has_perm(User, 'change', user_staff, obj)
        assert not has_perm(User, 'delete', user_staff)
        assert not has_perm(User, 'delete', user_staff, obj)

    def test_user_blog_author(self, user_blog_author, obj):
        assert not has_perm(User, 'add', user_blog_author)
        assert not has_perm(User, 'view', user_blog_author)
        assert not has_perm(User, 'view', user_blog_author, obj)
        assert not has_perm(User, 'change', user_blog_author)
        assert not has_perm(User, 'change', user_blog_author, obj)
        assert not has_perm(User, 'delete', user_blog_author)
        assert not has_perm(User, 'delete', user_blog_author, obj)

    def test_user_blog_admin(self, user_blog_admin, obj):
        assert has_perm(User, 'add', user_blog_admin)
        assert has_perm(User, 'view', user_blog_admin)
        assert has_perm(User, 'view', user_blog_admin, obj)
        assert has_perm(User, 'change', user_blog_admin)
        assert has_perm(User, 'change', user_blog_admin, obj)
        assert not has_perm(User, 'delete', user_blog_admin)
        assert not has_perm(User, 'delete', user_blog_admin, obj)

    def test_user_app_admin(self, user_app_admin, obj):
        assert has_perm(User, 'add', user_app_admin)
        assert has_perm(User, 'view', user_app_admin)
        assert has_perm(User, 'view', user_app_admin, obj)
        assert has_perm(User, 'change', user_app_admin)
        assert has_perm(User, 'change', user_app_admin, obj)
        assert has_perm(User, 'delete', user_app_admin)
        assert has_perm(User, 'delete', user_app_admin, obj)

    def test_override(self, user_generic, obj):
        override_perms(User, {
            'add': rules.always_allow,
            'view': rules.always_allow,
            'change': rules.always_allow,
            'delete': rules.always_allow,
        })
        assert has_perm(User, 'add', user_generic)
        assert has_perm(User, 'view', user_generic)
        assert has_perm(User, 'view', user_generic, obj)
        assert has_perm(User, 'change', user_generic, obj)
        assert has_perm(User, 'change', user_generic, obj)
        assert has_perm(User, 'delete', user_generic, obj)
        assert has_perm(User, 'delete', user_generic, obj)


class TestAppRolePerms:
    @pytest.fixture
    def user_blog_author(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_author', is_staff=True)
        BlogAuthorProfile.objects.create(user=user)
        return user

    @pytest.fixture
    def user_blog_author_privileged(self, django_user_model):
        user = django_user_model.objects.create(username='user_blog_author_privileged', is_staff=True)
        BlogAuthorProfile.objects.create(user=user, is_privileged=True)
        return user

    @pytest.fixture
    def obj(self, django_user_model):
        user = django_user_model.objects.create(username='username')
        return BlogAuthorProfile.objects.create(user=user)

    def test_user_blog_author(self, user_blog_author, obj):
        assert not has_perm(BlogAuthorProfile, 'add', user_blog_author)
        assert has_perm(BlogAuthorProfile, 'view', user_blog_author)
        assert has_perm(BlogAuthorProfile, 'view', user_blog_author, obj)
        assert has_perm(BlogAuthorProfile, 'change', user_blog_author)
        assert not has_perm(BlogAuthorProfile, 'change', user_blog_author, obj)
        assert has_perm(BlogAuthorProfile, 'change', user_blog_author,
                        BlogAuthorProfile.objects.get(user=user_blog_author))
        assert not has_perm(BlogAuthorProfile, 'delete', user_blog_author)
        assert not has_perm(BlogAuthorProfile, 'delete', user_blog_author, obj)

    def test_user_blog_author_privileged(self, user_blog_author_privileged, obj):
        assert has_perm(BlogAuthorProfile, 'add', user_blog_author_privileged)
