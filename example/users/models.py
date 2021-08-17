import rules
from django.contrib.auth.models import AbstractUser
from rules.contrib.models import RulesModel

from iam.mixins import IAMUserMixin


class User(
    IAMUserMixin,
    AbstractUser,
    RulesModel
):
    class Meta(AbstractUser.Meta):
        rules_permissions = {
            'add': rules.is_staff,
            'change': rules.is_staff,
            'view': rules.is_staff,
            'delete': rules.is_staff,
        }
