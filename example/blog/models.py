from django.contrib.auth import get_user_model
from rules.contrib.models import RulesModel

from iam.factories import AbstractProfileFactory
from users.models import AdminProfile
from .rules import is_blog_admin

User = get_user_model()


class BlogAdminProfile(
    AbstractProfileFactory.as_abstract_model('blog_admin_profile'),
    RulesModel
):
    parent = AdminProfile

    class Meta:
        rules_permissions = {
            'add': is_blog_admin,
            'view': is_blog_admin,
            'change': is_blog_admin,
            'delete': is_blog_admin,
        }
