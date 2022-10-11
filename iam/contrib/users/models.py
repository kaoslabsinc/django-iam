from dj_kaos_utils.models.mixins import HasInitials
from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db.models import Value
from django.db.models.functions import Concat
from rules.contrib.models import RulesModel

from iam.mixins import IAMUserMixin


class AbstractBaseIAMUser(
    IAMUserMixin,
    AbstractBaseUser
):
    """
    Abstract base user class that implements the `IAMUserMixin` interface to interact with IAM.
    """

    class Meta(AbstractBaseUser.Meta):
        abstract = True


class AbstractIAMUser(
    HasInitials,
    IAMUserMixin,
    AbstractUser,
    RulesModel
):
    """
    Abstract base user class that implements the `IAMUserMixin` interface to interact with IAM, inherits from
    `RulesModel` to manage its permissions using `rules`, plus a few handy properties.
    """

    class Meta(AbstractUser.Meta):
        abstract = True

    take_initials_from = 'display_name'
    id_field = 'username'

    @property
    @admin.display(ordering=Concat('first_name', Value(' '), 'last_name'))
    def full_name(self):
        """
        :return: Return the user's full name (i.e. `first_name` + `last_name`)
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        """
        :return: The best way to display this user's name in a UI. Default to their full name if it exists,
        otherwise their username.
        """
        return self.full_name if self.full_name.strip() else self.username

    @property
    def display_id(self):
        """
        :return: The best string of characters to id this user on a UI. Defaults to ``instance.username``. Change
        `.id_field` to use a different field for id (e.g. `email`).
        """
        return getattr(self, self.id_field)


__all__ = [
    'AbstractBaseIAMUser',
    'AbstractIAMUser',
]
