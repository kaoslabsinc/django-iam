import rules

from iam.registry import get_registered_roles

p_system = rules.always_deny


def is_any_helper(check_role_conf):
    passing_roles = get_registered_roles(check_role_conf)
    return lambda user: any(profile_model_cls.get_predicate().test(user) for profile_model_cls in passing_roles)


@rules.predicate
def is_any_admin(user):
    return is_any_helper(lambda conf: conf.get('admin'))(user)
