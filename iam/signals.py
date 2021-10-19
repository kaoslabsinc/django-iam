import django.contrib.auth.apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from iam.models import Role


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if isinstance(sender, django.contrib.auth.apps.AuthConfig):
        from django.apps import apps
        for app_config in apps.get_app_configs():
            if rules_module := getattr(app_config.module, 'rules', None):
                if roles := getattr(rules_module, 'Roles', None):
                    for attr in dir(roles):
                        if isinstance(role := getattr(roles, attr), Role):
                            role.upgrade_from_db()
