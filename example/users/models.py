from django.contrib.auth.models import AbstractUser
from rules.contrib.models import RulesModel

from iam.factories import AbstractProfileFactory
from iam.mixins import IAMUserMixin
from iam.utils import override_perms


class AdminProfile(
    AbstractProfileFactory.as_abstract_model(related_name='admin_profile'),
    RulesModel
):
    pass


is_admin = AdminProfile.get_predicate()
override_perms(AdminProfile, {
    'add': is_admin,
    'view': is_admin,
    'change': is_admin,
    'delete': is_admin,
})


class User(IAMUserMixin, AbstractUser, RulesModel):
    class Meta(AbstractUser.Meta):
        rules_permissions = {
            'add': is_admin,
            'view': is_admin,
            'change': is_admin,
            'delete': is_admin,
        }
