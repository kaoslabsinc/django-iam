Advanced Setup
**************

.. highlight:: python

``models.py``::

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


    class BlogPost(RulesModel):
        owner = models.ForeignKey(AuthorProfile, models.PROTECT, 'blogs')

        class Meta:
            rules_permissions = {
                'add': is_author,
                'view': is_super_author | is_author,
                'change': is_super_author | (is_author & is_owner),
                'delete': is_super_author,
            }

``rules.py``::

    import rules

    from iam.utils import lazy_get_predicate

    rules.add_perm('blog', rules.is_staff)

    is_author = lazy_get_predicate('blog.AuthorProfile')
    is_super_author = lazy_get_predicate('blog.AuthorProfile', lambda p: p.is_super_author)
