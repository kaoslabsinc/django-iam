from building_blocks.models import HasInitials
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
    class Meta:
        abstract = True


class AbstractIAMUser(
    HasInitials,
    IAMUserMixin,
    AbstractUser,
    RulesModel
):
    class Meta(AbstractUser.Meta):
        abstract = True

    take_initials_from = 'display_name'

    @property
    @admin.display(ordering=Concat('first_name', Value(' '), 'last_name'))
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        return self.full_name if self.full_name.strip() else self.username
