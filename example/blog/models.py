from django.contrib.auth import get_user_model
from rules.contrib.models import RulesModel

from iam.factories import AbstractProfileFactory
from iam.registry import register_role
from users.models import AppAdminProfile
from .rules import is_blog_admin, is_blog_author

User = get_user_model()


@register_role(admin=True)
class BlogAdminProfile(
    AbstractProfileFactory.as_abstract_model('blog_admin_profile'),
    RulesModel
):
    parent = AppAdminProfile

    class Meta:
        rules_permissions = {
            'add': is_blog_admin,
            'view': is_blog_admin,
            'change': is_blog_admin,
            'delete': is_blog_admin,
        }


@register_role
class BlogAuthorProfile(
    AbstractProfileFactory.as_abstract_model('blog_author_profile'),
    RulesModel
):
    parent = BlogAdminProfile

    class Meta:
        rules_permissions = {
            'add': is_blog_admin,
            'view': is_blog_author,
            'change': is_blog_admin,
            'delete': is_blog_admin,
        }
