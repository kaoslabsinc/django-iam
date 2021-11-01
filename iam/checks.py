from django.apps import apps
from django.contrib.auth.models import Group
from django.core.checks import Error, register, Tags

from iam.models import Role


@register(Tags.models)
def my_check(app_configs, **kwargs):
    errors = []
    if app_configs is None:
        app_configs = apps.get_app_configs()
    for app_config in app_configs:
        if rules_module := getattr(app_config.module, 'rules', None):
            if roles := getattr(rules_module, 'Roles', None):
                for attr in dir(roles):
                    if isinstance(role := getattr(roles, attr), Role):
                        try:
                            Group.objects.get(name=role.name)
                        except Group.DoesNotExist:
                            errors.append(
                                Error(
                                    f"Group '{role.name}' does not exists.",
                                    hint="Run manage.py migrate iam --skip-checks",
                                    obj=role,
                                    id="iam.E001"
                                )
                            )
    return errors
