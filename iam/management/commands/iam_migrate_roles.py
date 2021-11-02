from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    requires_system_checks = []

    def handle(self, *args, **options):
        call_command('migrate', 'iam', skip_checks=True)
