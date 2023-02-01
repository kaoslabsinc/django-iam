from typing import Optional

import rules
from django.db import models

from .registry import get_registered_roles


class RolePredicateMixin(models.Model):
    """
    Mixin used on profile classes. Provides class method `get_predicate` to create rules predicates to check if a user
    has a profile or not.
    Provides `parent` attribute. If a role has a parent, and a user has the parent profile, the user will have all
    permissions associated with the child role too.

    :param parent: A role could be a specific subset of another parent role. Set parent to that. If a user has a role
        that is the child of another roles, they automatically get all the permissions for the parent role too.
    """
    parent: 'RolePredicateMixin' = None

    class Meta:
        abstract = True

    @classmethod
    def get_predicate(cls, extra_check=None):
        """
        Return a rules predicate that checks if a user has a corresponding profile thus having that role.

        :param extra_check: Optionally check extra parameters on the user's profile instance.
        :return: Predicate
        """

        def has_role(user):
            if user.is_superuser:
                return True

            profile_instance = user.get_or_set_role(cls._meta.model)
            return bool(profile_instance) and (not extra_check or extra_check(profile_instance))

        role_name = cls._meta.verbose_name.rstrip(' profile').replace(' ', '_')
        predicate = rules.predicate(has_role, name=f'is_{role_name}')
        if cls.parent:
            return predicate | cls.parent.get_predicate(extra_check)
        return predicate


class IAMUserMixin:
    """
    Mixin used on custom user models that use IAM for their permission management. Provides interfaces to the user model
    to interact with the IAM, and cache permissions.
    """

    def __init__(self, *args, **kwargs):
        self._roles = {}  # { ProfileModel: instance | False }
        super(IAMUserMixin, self).__init__(*args, **kwargs)

    @property
    def roles(self):
        return self._roles

    def _set_role(self, model_cls) -> Optional[RolePredicateMixin]:
        """
        Check if this user has a particular profile denoted by `model_cls`. If they do, cache the profile instance. If
        not cache a False value, so we don't need to hit the database again for this check.

        :param model_cls: The model class of the profile to be checked.
        :return: The profile instance belonging to the user or False
        """
        try:
            profile_instance = model_cls.objects.available().get(user=self)
        except model_cls.DoesNotExist:
            profile_instance = False
        self._roles[model_cls] = profile_instance
        return profile_instance

    def get_or_set_role(self, model_cls):
        """
        Check if this user has a particular profile denoted by `model_cls`.

        First hit the cache. If there is no value
        in the cache, hit the database. If the user has the profile, cache the profile instance. If
        not, cache a False value, so we don't need to hit the database again for this check.

        :param model_cls: The model class of the profile to be checked.
        :return: The profile instance belonging to the user or None
        """
        profile_instance = self.roles.get(model_cls)  # None | False | instance
        if profile_instance is None:
            profile_instance = self._set_role(model_cls)
        return profile_instance if profile_instance else None

    def load_roles(self):
        """
        Load all the roles (and profiles) this user has in their cache.
        """
        self._roles = {}
        for model_cls in get_registered_roles():
            self._set_role(model_cls)
