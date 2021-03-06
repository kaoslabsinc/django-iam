from building_blocks.factories import HasNameFactory, HasDescriptionFactory
from django.contrib.auth import get_user_model
from django.db import models
from rules.contrib.models import RulesModel

from iam import register_role
from iam.contrib.utils import get_profile_cls_verbose_name_plural
from iam.factories import AbstractProfileFactory, HasOwnerFactory
from iam.predicates import is_owner, is_user
from users.models import AppAdminProfile
from .rules import is_blog_admin, is_blog_author, is_privileged_blog_author

User = get_user_model()


@register_role(admin=True)
class BlogAdminProfile(
    AbstractProfileFactory.as_abstract_model('blog_admin_profile'),
    RulesModel
):
    parent = AppAdminProfile

    class Meta:
        verbose_name_plural = get_profile_cls_verbose_name_plural('BlogAdminProfile')
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

    is_privileged = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = get_profile_cls_verbose_name_plural('BlogAuthorProfile')
        rules_permissions = {
            'add': is_privileged_blog_author | is_blog_admin,
            'view': is_blog_author,
            'change': is_blog_author & is_user,
            'delete': is_blog_admin,
        }


class BlogPost(
    HasNameFactory.as_abstract_model(),
    HasOwnerFactory.as_abstract_model(BlogAuthorProfile, owner_alias='author', related_name='blog_posts'),
    HasDescriptionFactory.as_abstract_model(),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_blog_author,
            'view': is_blog_author,
            'change': is_blog_admin | is_blog_author & is_owner,
            'delete': is_blog_admin | is_blog_author & is_owner,
        }
