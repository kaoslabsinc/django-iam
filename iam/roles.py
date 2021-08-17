import rules
from django.apps import apps
from django.utils.text import camel_case_to_spaces


def _model_path_to_name(model_path):
    model_name = model_path.split('.')[-1]
    return camel_case_to_spaces(model_name).replace(' ', '_')


class Role:
    def __init__(self, profile_model_path, name=None, verbose_name=None):
        self._profile_model = None
        self._profile_model_path = profile_model_path
        self.name = name or _model_path_to_name(self._profile_model_path)
        self.verbose_name = verbose_name or self.name.replace('_', ' ').title()

    @property
    def profile_model(self):
        if not self._profile_model:
            self._profile_model = apps.get_model(self._profile_model_path)
        return self._profile_model

    def get_predicate(self, *args):
        def is_role(user):
            return user.has_role(self, *args)

        return rules.predicate(is_role, name=f'is_{self.name}')

    @property
    def predicate(self):
        return self.get_predicate()

    def __str__(self):
        return f"Role: {self.name}"

    def __repr__(self):
        return self.__str__()
