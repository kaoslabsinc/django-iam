from django.contrib.auth.models import AbstractUser
from rules.contrib.models import RulesModel

from iam.factories import AbstractProfileFactory
from iam.mixins import IAMUserMixin
from iam.registry import register_role
from .rules import is_admin


@register_role
class AdminProfile(
    AbstractProfileFactory.as_abstract_model(related_name='admin_profile'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_admin,
            'view': is_admin,
            'change': is_admin,
            'delete': is_admin,
        }


class User(IAMUserMixin, AbstractUser, RulesModel):
    class Meta(AbstractUser.Meta):
        rules_permissions = {
            'add': is_admin,
            'view': is_admin,
            'change': is_admin,
            'delete': is_admin,
        }
