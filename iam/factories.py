from building_blocks.models import Archivable
from building_blocks.models.factories import AbstractModelFactory, HasUserFactory
from django.db import models


class AbstractProfileFactory(AbstractModelFactory):
    @staticmethod
    def as_abstract_model(related_name=None, user_optional=False):
        class AbstractProfile(
            Archivable,
            HasUserFactory.as_abstract_model(related_name=related_name, one_to_one=True, optional=user_optional),
            models.Model
        ):
            class Meta:
                abstract = True

            def __str__(self):
                return f"{self.user}'s {self._meta.verbose_name}"

        return AbstractProfile
