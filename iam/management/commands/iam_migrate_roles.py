from django.core.management.base import BaseCommand

from iam.utils import create_role_groups


class Command(BaseCommand):
    requires_system_checks = []

    def handle(self, *args, **options):
        create_role_groups()
