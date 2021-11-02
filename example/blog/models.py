from building_blocks.models.factories import HasNameFactory, HasDescriptionFactory
from django.conf import settings
from django.db import models
from rules.contrib.models import RulesModel

from blog.rules import is_blog_author, is_posts_author


class BlogPost(
    HasNameFactory.as_abstract_model(),
    HasDescriptionFactory.as_abstract_model(),
    RulesModel
):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        rules_permissions = {
            'add': is_blog_author,
            'view': is_blog_author,
            'change': is_blog_author & is_posts_author,
            'delete': is_blog_author & is_posts_author,
        }
