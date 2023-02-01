import pytest

from iam.contrib.predicates import is_any_admin
from simple.models import AuthorProfile


class TestIsAny:
    @pytest.fixture
    def user(self, create_user):
        return create_user()

    @pytest.fixture
    def user_author(self, create_user):
        user = create_user()
        AuthorProfile.objects.create(user=user)
        return user

    def test_is_any_admin(self, user, user_author):
        assert not is_any_admin(user)
        assert not is_any_admin(user_author)
