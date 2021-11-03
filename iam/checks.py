from django.contrib.auth.models import Group
from django.core.checks import Warning, register

from .utils import get_all_roles


class Tags:
    iam = 'iam'


@register(Tags.iam)
def check_role_groups(app_configs, **kwargs):
    errors = []
    for role in get_all_roles(app_configs):
        try:
            Group.objects.get(name=role.name)
        except Group.DoesNotExist:
            errors.append(
                Warning(
                    f"Group '{role.name}' does not exist.",
                    hint="Run manage.py iam_migrate_roles",
                    obj=role,
                    id='iam.W001'
                )
            )
    return errors
