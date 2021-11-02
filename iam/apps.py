from django.apps import AppConfig, apps


class IAMConfig(AppConfig):
    name = 'iam'

    def ready(self):
        from django.contrib.auth.models import Group
        from . import signals  # NoQA
        from . import checks  # NoQA

        for app_config in apps.get_app_configs():
            if rules_module := getattr(app_config.module, 'rules', None):
                if roles := getattr(rules_module, 'Roles', None):
                    for attr in dir(roles):
                        from iam.models import Role
                        if isinstance(role := getattr(roles, attr), Role):
                            try:
                                role.refresh_from_db()
                            except Group.DoesNotExist:
                                # IAMConfig.ready() is called before checks.check_role_groups(). We can safely ignore
                                # the missing Group here because it will be flagged by check_role_groups() later
                                pass
