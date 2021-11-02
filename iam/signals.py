from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .apps import IAMConfig
from .utils import create_role_groups


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if isinstance(sender, IAMConfig):
        create_role_groups()
