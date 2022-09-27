import pytest

from simple.models import AuthorProfile, BlogPost
from tests.helpers import assert_has_perm_bulk


class TestBlogPostPerms:
    @pytest.fixture
    def user_generic(self, create_user):
        return create_user('user_generic')

    @pytest.fixture
    def user_author_nonowner(self, create_user, create_profile):
        user = create_user('user_author_nonowner')
        create_profile(AuthorProfile, user)
        return user

    @pytest.fixture
    def user_author_owner(self, create_user, create_profile):
        user = create_user('user_author_owner')
        create_profile(AuthorProfile, user)
        return user

    @pytest.fixture
    def user_super_author(self, create_user, create_profile):
        user = create_user('user_super_author')
        create_profile(AuthorProfile, user, is_super_author=True)
        return user

    @pytest.fixture
    def user_superuser(self, create_user):
        return create_user('user_superuser', is_superuser=True)

    @pytest.fixture
    def obj(self, user_author_owner):
        owner = AuthorProfile.objects.get(user=user_author_owner)
        return BlogPost.objects.get_or_create(owner=owner)[0]

    def test_user_generic(self, user_generic, obj):
        assert_has_perm_bulk(BlogPost, user_generic, obj, {
            'add': (False, None),
            'view': (False, False),
            'change': (False, False),
            'delete': (False, False),
        })

    def test_user_author_nonowner(self, user_author_nonowner, obj):
        assert_has_perm_bulk(BlogPost, user_author_nonowner, obj, {
            'add': (True, None),
            'view': (True, True),
            'change': (True, False),
            'delete': (False, False),
        })

    def test_user_author_owner(self, user_author_owner, obj):
        assert_has_perm_bulk(BlogPost, user_author_owner, obj, {
            'add': (True, None),
            'view': (True, True),
            'change': (True, True),
            'delete': (False, False),
        })

    def test_user_super_author(self, user_super_author, obj):
        assert_has_perm_bulk(BlogPost, user_super_author, obj, {
            'add': (True, None),
            'view': (True, True),
            'change': (True, True),
            'delete': (True, True),
        })

    def test_user_superuser(self, user_superuser, obj):
        assert_has_perm_bulk(BlogPost, user_superuser, obj, {
            'add': (True, None),
            'view': (True, True),
            'change': (True, True),
            'delete': (True, True),
        })
