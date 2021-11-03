import rules
from django.db import models

DEFAULT_EXTRA_CHECK = lambda x: True  # NoQA


class RolePredicateMixin(models.Model):
    parent: 'RolePredicateMixin' = None

    class Meta:
        abstract = True

    @classmethod
    def get_predicate(cls, extra_check=DEFAULT_EXTRA_CHECK):
        def has_role(user):
            model_cls = cls._meta.model
            profile_instance = user.roles.get(model_cls)  # None, False, instance
            if profile_instance is None:
                try:
                    profile_instance = model_cls.objects.active().get(user=user)
                except model_cls.DoesNotExist:
                    profile_instance = False
                finally:
                    user.set_role(model_cls, profile_instance)
            return bool(profile_instance) and extra_check(profile_instance)

        role_name = cls._meta.verbose_name.rstrip(' profile').replace(' ', '_')
        predicate = rules.predicate(has_role, name=f'is_{role_name}')
        if cls.parent:
            return predicate | cls.parent.get_predicate(extra_check)
        return predicate
