from django.core.management.commands.migrate import Command as MigrateCommand

from iam.checks import Tags


class Command(MigrateCommand):
    skip_checks = [Tags.iam]

    def check(self, tags=None, **kwargs):
        super(Command, self).check(tags=tags, **kwargs)
