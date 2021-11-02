from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .apps import IAMConfig
from .utils import get_all_roles


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if isinstance(sender, IAMConfig):
        for role in get_all_roles():
            Group.objects.get_or_create(name=role.name)
