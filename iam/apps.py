from django.apps import AppConfig
from django.db import connections

from .models import Role


def table_exists(table_name: str, connection_name: str = 'default') -> bool:
    return table_name in connections[connection_name].introspection.table_names()


class IAMConfig(AppConfig):
    name = 'iam'

    def ready(self):
        if not table_exists('auth_group'):
            return
        from django.apps import apps
        for app_config in apps.get_app_configs():
            if rules_module := getattr(app_config.module, 'rules', None):
                if roles := getattr(rules_module, 'Roles', None):
                    for attr in dir(roles):
                        if isinstance(role := getattr(roles, attr), Role):
                            role.group  # NoQA
