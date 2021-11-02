from django.apps import AppConfig

from .utils import get_all_roles


class IAMConfig(AppConfig):
    name = 'iam'

    def ready(self):
        from django.contrib.auth.models import Group
        from . import signals  # NoQA
        from . import checks  # NoQA

        for role in get_all_roles():
            try:
                role.refresh_from_db()
            except Group.DoesNotExist:
                # IAMConfig.ready() is called before checks.check_role_groups(). We can safely ignore
                # the missing Group here because it will be flagged by check_role_groups() later
                pass
