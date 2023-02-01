import rules

from .predicates import p_system


class Perms:
    """
    A utility class with common `rules_permissions` (from `rules.RulesModel` interface) values.

    Example:
        >>> class MyModel(RulesModel):
        ...     class Meta:
        ...         rules_permissions = Perms.all_is_staff
    """
    all_is_staff = {
        'add': rules.is_staff,
        'change': rules.is_staff,
        'view': rules.is_staff,
        'delete': rules.is_staff,
    }

    staff_readonly = {
        'add': p_system,
        'view': rules.is_staff,
        'change': p_system,
        'delete': p_system,
    }
