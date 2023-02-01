import rules
from django.apps import apps
from django.utils.text import camel_case_to_spaces

from .mixins import RolePredicateMixin


def override_perms(cls, new_rules: dict):
    """
    Override `rules_permissions` for the class with new rules.
    :param cls: The model class where we want to override permissions.
    :param new_rules: The new set of rules.

    Example:
        >>> override_perms(SomeModel, {'add': is_owner})
    """
    for perm, rule in new_rules.items():
        rules.set_perm(cls.get_perm(perm), rule)


def _model_path_to_name(model_path):
    model_name = model_path.split('.')[-1]
    return camel_case_to_spaces(model_name).replace(' ', '_')


def lazy_get_predicate(model_path, extra_check=None):
    """
    Return a lazy predicate that checks whether a user has a profile or not.

    :param model_path: dot path to the model, used to lazily load the model, without referencing it directly.
    :param extra_check: Extra check on the profile instance.
    :return: Predicate

    Example:
        >>> is_author = lazy_get_predicate('blog.AuthorProfile')
        >>> is_super_author = lazy_get_predicate('blog.AuthorProfile', lambda p: p.is_super_author)
    """

    def check(*args, **kwargs):
        model_cls: RolePredicateMixin = apps.get_model(model_path)
        predicate = model_cls.get_predicate(extra_check)
        return predicate.test(*args, **kwargs)

    role_name = _model_path_to_name(model_path).rstrip('_profile')
    return rules.predicate(check, name=f'is_{role_name}')
