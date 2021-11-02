from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group in Group.objects.all():
            if group.user_set.count() == 0:
                group.delete()
                self.stdout.write(self.style.SUCCESS(f"Deleted unused Group {group.name}"))
