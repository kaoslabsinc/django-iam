from building_blocks.models import Archivable
from building_blocks.models.factories import AbstractModelFactory, HasUserFactory
from building_blocks.models.utils import generate_field_kwargs
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
                return f"{self.user}'s {self._meta.verbose_name}"

            def deactivate(self):
                return self.archive()

        return AbstractProfile


class HasOwnerFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(owner_profile_class, related_name=None,
                          one_to_one=False, optional=False, on_delete=None):
        owner_field_cls, on_delete = AbstractModelFactory._get_fk_params(one_to_one, optional, on_delete)

        class HasOwner(models.Model):
            class Meta:
                abstract = True

            owner = owner_field_cls(owner_profile_class, on_delete=on_delete, related_name=related_name,
                                    **generate_field_kwargs(optional_null=optional))

        return HasOwner
