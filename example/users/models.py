import rules
from django.contrib.auth.models import AbstractUser
from rules.contrib.models import RulesModel

from iam.contrib.users.models import AbstractIAMUser


class User(AbstractIAMUser):
    class Meta(AbstractIAMUser.Meta):
        rules_permissions = {
            'add': rules.is_staff,
            'change': rules.is_staff,
            'view': rules.is_staff,
            'delete': rules.is_staff,
        }
