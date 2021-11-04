from django.contrib.auth.models import AbstractUser
from rules.contrib.models import RulesModel

from iam.contrib.users.models import AbstractIAMUser
from iam.factories import AbstractProfileFactory
from iam.predicates import is_admin_role
from iam.registry import register_role
from .rules import is_app_admin


@register_role(admin=True)
class AppAdminProfile(
    AbstractProfileFactory.as_abstract_model(related_name='app_admin_profile'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_app_admin,
            'view': is_app_admin,
            'change': is_app_admin,
            'delete': is_app_admin,
        }


class User(AbstractIAMUser):
    class Meta(AbstractIAMUser.Meta):
        rules_permissions = {
            'add': is_admin_role,
            'view': is_admin_role,
            'change': is_admin_role,
            'delete': is_app_admin,
        }
