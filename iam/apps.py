from django.apps import AppConfig

from django.apps import apps

class IAMConfig(AppConfig):
    name = 'iam'

    def ready(self):
        from . import signals  # NoQA
        from . import checks  # NoQA

