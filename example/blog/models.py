from building_blocks.models.factories import HasNameFactory, HasDescriptionFactory
from rules import is_superuser
from rules.contrib.models import RulesModel

from blog.rules import is_blog_manager, is_blog_author
from iam.factories import AbstractProfileFactory, HasOwnerFactory
from iam.predicates import is_owner, is_user


class BlogManager(
    AbstractProfileFactory.as_abstract_model(related_name='blog_manager_profile'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_superuser,
            'view': is_blog_manager,
            'change': is_superuser,
            'delete': is_superuser,
        }


class BlogAuthor(
    AbstractProfileFactory.as_abstract_model(related_name='blog_author_profile'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_blog_manager,
            'view': is_blog_author & is_user | is_blog_manager,
            'change': is_blog_manager,
            'delete': is_blog_manager,
        }


class BlogPost(
    HasNameFactory.as_abstract_model(),
    HasDescriptionFactory.as_abstract_model(),
    HasOwnerFactory.as_abstract_model(BlogAuthor, related_name='blog_posts'),
    RulesModel
):
    class Meta:
        rules_permissions = {
            'add': is_blog_author | is_blog_manager,
            'view': is_blog_author & is_owner | is_blog_manager,
            'change': is_blog_author & is_owner | is_blog_manager,
            'delete': is_blog_author & is_owner | is_blog_manager,
        }
