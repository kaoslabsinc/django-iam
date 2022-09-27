from django.contrib.auth.models import AbstractUser

from iam.mixins import IAMUserMixin


class User(
    IAMUserMixin,
    AbstractUser
):
    pass
