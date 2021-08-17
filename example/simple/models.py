import rules
from django.conf import settings
from django.db import models
from rules.contrib.models import RulesModel

from simple.rules import is_simple_manager


class SimpleManager(
    RulesModel
):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        rules_permissions = {
            'add': rules.is_superuser,
            'view': rules.is_superuser | is_simple_manager,
            'change': rules.is_superuser,
            'delete': rules.is_superuser,
        }


class SimpleModel(
    RulesModel
):
    name = models.CharField(max_length=100)

    class Meta:
        rules_permissions = {
            'add': is_simple_manager,
            'view': is_simple_manager,
            'change': is_simple_manager,
            'delete': is_simple_manager,
        }


class SimpleProxy(
    SimpleModel
):
    class Meta:
        proxy = True
        rules_permissions = {
            'add': rules.is_superuser,
            'view': rules.is_superuser,
            'change': rules.is_superuser,
            'delete': rules.is_superuser,
        }
