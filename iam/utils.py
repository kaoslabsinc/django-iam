import rules
from django.apps import apps


def override_perms(cls, new_rules):
    for perm, rule in new_rules.items():
        rules.set_perm(cls.get_perm(perm), rule)


def get_all_roles(app_configs=None):
    from .models import Role

    if app_configs is None:
        app_configs = apps.get_app_configs()
    all_roles = []
    for app_config in app_configs:
        if rules_module := getattr(app_config.module, 'rules', None):
            if roles := getattr(rules_module, 'Roles', None):
                for attr in dir(roles):
                    if isinstance(role := getattr(roles, attr), Role):
                        all_roles.append(role)
    return all_roles


def create_role_groups():
    from django.contrib.auth.models import Group

    created_groups = []
    for role in get_all_roles():
        group, created = Group.objects.get_or_create(name=role.name)
        if created:
            created_groups.append(group)
    return created_groups

