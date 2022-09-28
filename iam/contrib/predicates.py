import rules

from iam.registry import get_registered_roles

p_system = rules.always_deny


def is_any_helper(check_role_conf):
    """
    Check if any of the profiles this user belongs to pass `check_role_conf(role_conf)`
    :param check_role_conf: Function that returns true if a particular role_conf passes a certain criteria.
    :return: A function that receives a user and returns if they belong to the roles we want qualified by
    `check_role_conf`.
    """
    passing_roles = get_registered_roles(check_role_conf)
    return lambda user: any(profile_model_cls.get_predicate().test(user) for profile_model_cls in passing_roles)


@rules.predicate
def is_any_admin(user):
    """
    Predicate to check if this user belongs to a role that has admin=True.
    """
    return is_any_helper(lambda conf: conf.get('admin') is True)(user)
