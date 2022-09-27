from django.apps import AppConfig


class IAMConfig(AppConfig):
    name = 'iam'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        from . import registry  # NoQA
        autodiscover_modules('rules')
