import rules

from iam.contrib.users.models import AbstractIAMUser
from .rules import is_admin


class User(AbstractIAMUser):
    class Meta(AbstractIAMUser.Meta):
        rules_permissions = {
            'add': is_admin,
            'change': is_admin,
            'view': rules.is_staff,
            'delete': is_admin,
        }
