from iam.registry import get_registered_roles
from simple.models import AuthorProfile


def test_UserProfileModel(django_user_model):
    user = django_user_model.objects.create()
    profile = AuthorProfile.objects.create(user=user)
    assert profile.user == user
    assert profile.is_available


def test_registry():
    registered_roles = get_registered_roles()
    assert AuthorProfile in registered_roles
