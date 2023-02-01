from django.contrib.auth.models import AbstractUser

from iam.contrib.users.models import AbstractIAMUser


class User(
    AbstractIAMUser
):
    pass
