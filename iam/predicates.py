import rules

from iam.registry import get_admin_roles


@rules.predicate
def is_admin_role(user):
    return any(profile_model_cls.get_predicate().test(user) for profile_model_cls in get_admin_roles())


@rules.predicate
def is_owner(user, obj):
    return obj is None or obj.owner.user == user
