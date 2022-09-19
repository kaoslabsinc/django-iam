from django.contrib.auth.checks import check_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from rules.contrib.models import RulesModel

from iam.models import UserProfileModel
from iam.predicates import is_owner
from iam.registry import register_role
from .rules import is_author, is_super_author


@register_role
class AuthorProfile(UserProfileModel):
    is_super_author = models.BooleanField(default=False)

    @staticmethod
    def check_super_author(user):
        return AuthorProfile.check_user(lambda p: p.is_super_author)(user)


class BlogPost(RulesModel):
    owner = models.ForeignKey(AuthorProfile, models.PROTECT, 'blogs')

    class Meta:
        rules_permissions = {
            'add': is_author,
            'view': is_super_author | is_author,
            'change': is_super_author | (is_author & is_owner),
            'delete': is_super_author,
        }
