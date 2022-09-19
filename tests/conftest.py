import pytest
from django.utils.crypto import get_random_string


@pytest.fixture
def create_user(django_user_model):
    def _create_user(username=None, password=None, **kwargs):
        if username is None:
            username = get_random_string(12)
        user = django_user_model.objects.create_user(username, **kwargs)
        if password:
            user.set_password(password)
        return user

    return _create_user


@pytest.fixture
def create_profile():
    def _create_profile(profile_model, user, **kwargs):
        return profile_model.objects.create(user=user, **kwargs)

    return _create_profile
