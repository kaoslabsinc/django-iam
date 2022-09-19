from django.db import models
from rules.contrib.models import RulesModel

from iam.models import UserProfileModel
from iam.predicates import is_owner
from iam.registry import register_role
from .rules import is_author


@register_role
class AuthorProfile(UserProfileModel):
    pass


class BlogPost(RulesModel):
    owner = models.ForeignKey(AuthorProfile, models.PROTECT, 'blogs')

    class Meta:
        rules_permissions = {
            'add': is_author,
            'view': is_author,
            'change': is_author & is_owner,
            'delete': is_author & is_owner,
        }
