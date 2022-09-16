from building_blocks.models import Archivable
from django.conf import settings
from django.db import models

from .mixins import RolePredicateMixin


class UserProfileModel(
    RolePredicateMixin,
    Archivable,
    models.Model
):
    class Meta:
        abstract = True

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    deactivate = Archivable.archive

    def __str__(self):
        return f"{self.user} as {self._meta.verbose_name}"

    @classmethod
    def check_user(cls, check_func):
        def check_user_func(user):
            profile = user.get_or_set_role(cls)
            if not profile:
                return False
            return check_func(profile)

        return check_user_func


__all__ = [
    'UserProfileModel',
]
