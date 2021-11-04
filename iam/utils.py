import rules
from django.apps import apps
from django.utils.text import camel_case_to_spaces

from .abstracts import RolePredicateMixin, DEFAULT_EXTRA_CHECK


def override_perms(cls, new_rules):
    for perm, rule in new_rules.items():
        rules.set_perm(cls.get_perm(perm), rule)


def _model_path_to_name(model_path):
    model_name = model_path.split('.')[-1]
    return camel_case_to_spaces(model_name).replace(' ', '_')


def lazy_get_predicate(model_path, extra_check=DEFAULT_EXTRA_CHECK):
    def check(*args, **kwargs):
        model_cls: RolePredicateMixin = apps.get_model(model_path)
        predicate = model_cls.get_predicate(extra_check)
        return predicate.test(*args, **kwargs)

    role_name = _model_path_to_name(model_path).rstrip('_profile')
    return rules.predicate(check, name=f'is_{role_name}')
