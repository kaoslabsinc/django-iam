from django.core.management.base import BaseCommand

from iam.utils import create_role_groups


class Command(BaseCommand):
    requires_system_checks = []

    def handle(self, *args, **options):
        created_groups = create_role_groups()
        if created_groups:
            self.stdout.write(self.style.SUCCESS(f"Created groups {', '.join(map(str, created_groups))}"))
