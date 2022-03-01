from building_blocks.models import Archivable
from building_blocks.factories import AbstractModelFactory, HasUserFactory
from building_blocks.factories.utils import generate_field_kwargs
from django.db import models

from .abstracts import RolePredicateMixin


class AbstractProfileFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(related_name=None, user_optional=False):
        class AbstractProfile(
            RolePredicateMixin,
            Archivable,
            HasUserFactory.as_abstract_model(related_name=related_name, one_to_one=True, optional=user_optional),
            models.Model
        ):
            class Meta:
                abstract = True

            def __str__(self):
                return f"{self.user} as {self._meta.verbose_name}"

            def deactivate(self):
                return self.archive()

            @classmethod
            def check_user(cls, check_func):
                def check_user_func(user):
                    profile = user.get_or_set_role(cls)
                    if not profile:
                        return False
                    return check_func(profile)

                return check_user_func

        return AbstractProfile


class HasOwnerFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(owner_profile_class, owner_alias=None, related_name=None,
                          one_to_one=False, optional=False, on_delete=None, **kwargs):
        owner_field_cls, on_delete = AbstractModelFactory._get_fk_params(one_to_one, optional, on_delete)
        verbose_name = kwargs.pop('verbose_name', None)
        verbose_owner_alias = owner_alias.replace('_', ' ') if owner_alias is not None else None

        class HasOwner(models.Model):
            class Meta:
                abstract = True

            owner = owner_field_cls(owner_profile_class, on_delete=on_delete,
                                    verbose_name=verbose_name or verbose_owner_alias,
                                    related_name=related_name,
                                    **generate_field_kwargs(optional_null=optional), **kwargs)

        if owner_alias:
            setattr(HasOwner, owner_alias, property(lambda self: self.owner))
        return HasOwner


__all__ = [
    'AbstractProfileFactory',
    'HasOwnerFactory',
]
