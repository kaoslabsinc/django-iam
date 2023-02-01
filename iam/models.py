from typing import Callable, Any
from warnings import warn

from building_blocks.models import Archivable, UnnamedKaosModel
from django.conf import settings
from django.db import models

from .mixins import RolePredicateMixin


class UserProfileModel(
    RolePredicateMixin,
    Archivable,
    UnnamedKaosModel,
    models.Model
):
    """
    Abstract model for profile models to inherit from. Provides a one-to-one user field that points to the owner of a
    profile.
    Override the user field, if you'd like to set its `related_name` or set it to optional (e.g. for bot profiles)
    """

    class Meta:
        abstract = True

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    deactivate = Archivable.archive

    def __str__(self):
        return f"{self.user} as {self._meta.verbose_name}"

    @classmethod
    def check_user(cls, check_func) -> Callable[[Any], bool]:
        """
        Return a function that first, checks if a user has the role denoted by this profile class, and then runs
        `check_func` on the user's profile for this role to determine extra permissions.

        :param check_func: Function that receives a profile instance and checks if it passes a condition or not.
        :return: Function that accepts a user instance as an argument, and checks if they have the role and some extra
            conditions.

        Example:
            >>> # models.py
            >>> @register_role
            >>> class AuthorProfile(UserProfileModel):
            >>>     is_super_author = models.BooleanField(default=False)
            >>>
            >>>     @staticmethod
            >>>     def check_super_author(user):
            >>>         return AuthorProfile.check_user(lambda p: p.is_super_author)(user)
        """

        warn('This method is deprecated.', DeprecationWarning)

        def check_user_func(user) -> bool:
            profile = user.get_or_set_role(cls)
            if not profile:
                return False
            return check_func(profile)

        return check_user_func


__all__ = [
    'UserProfileModel',
]
