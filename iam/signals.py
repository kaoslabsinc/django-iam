from django.apps import apps
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .apps import IAMConfig
from .models import Role


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if isinstance(sender, IAMConfig):
        for app_config in apps.get_app_configs():
            if rules_module := getattr(app_config.module, 'rules', None):
                if roles := getattr(rules_module, 'Roles', None):
                    for attr in dir(roles):
                        if isinstance(role := getattr(roles, attr), Role):
                            Group.objects.get_or_create(name=role.name)
