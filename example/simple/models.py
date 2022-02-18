from building_blocks.factories import HasNameFactory
from django.contrib.auth import get_user_model
from rules.contrib.models import RulesModel

from iam import register_role
from iam.contrib.utils import get_profile_cls_verbose_name_plural
from iam.factories import AbstractProfileFactory, HasOwnerFactory
from simple.rules import is_simple_admin
from users.models import AppAdminProfile

User = get_user_model()


@register_role(admin=True)
class SimpleAdminProfile(
    AbstractProfileFactory.as_abstract_model('simple_admin_profile'),
    RulesModel
):
    parent = AppAdminProfile

    class Meta:
        verbose_name_plural = get_profile_cls_verbose_name_plural('SimpleAdminProfile')
        rules_permissions = {
            'add': is_simple_admin,
            'view': is_simple_admin,
            'change': is_simple_admin,
            'delete': is_simple_admin,
        }


class SimpleObject(
    HasNameFactory.as_abstract_model(),
    HasOwnerFactory.as_abstract_model(SimpleAdminProfile, related_name='simple_objects'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_simple_admin,
            'view': is_simple_admin,
            'change': is_simple_admin,
            'delete': is_simple_admin,
        }
