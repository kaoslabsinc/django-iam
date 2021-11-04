from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.checks.registry import registry

from iam.checks import Tags, check_role_groups


class Command(MigrateCommand):
    skip_checks = [Tags.iam]

    def check(self, tags=None, **kwargs):
        registry.registered_checks.remove(check_role_groups)
        super(Command, self).check(tags=tags, **kwargs)
