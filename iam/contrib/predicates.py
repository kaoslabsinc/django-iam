import rules

from iam.registry import get_registered_roles


@rules.predicate
def is_any_admin(user):
    admin_roles = get_registered_roles(lambda conf: conf.get('admin'))
    return any(profile_model_cls.get_predicate().test(user) for profile_model_cls in admin_roles)
