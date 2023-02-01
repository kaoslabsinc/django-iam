from iam.registry import get_registered_roles
from simple.models import AuthorProfile


def test_UserProfileModel(create_user):
    user = create_user('username')
    profile = AuthorProfile.objects.create(user=user)
    assert profile.user == user
    assert profile.is_available
    assert str(profile) == "username as author profile"

    assert AuthorProfile.get_for_user(user) is not None
    user2 = create_user()
    assert AuthorProfile.get_for_user(user2) is None


def test_registry():
    registered_roles = get_registered_roles()
    assert AuthorProfile in registered_roles
