import rules
from django.apps import apps


class Role:
    def __init__(self, name, profile_model_path, verbose_name=None):
        self._profile_model = None
        self.name = name
        self._profile_model_path = profile_model_path
        if verbose_name is None:
            verbose_name = name.replace('_', ' ').title()
        self.verbose_name = verbose_name

    @property
    def profile_model(self):
        if not self._profile_model:
            self._profile_model = apps.get_model(self._profile_model_path)
        return self._profile_model

    def get_predicate(self, privileged=False):
        def is_role(user):
            return user.has_role(self, privileged=privileged)

        return rules.predicate(is_role, name=f'is_{self.name}')

    @property
    def predicate(self):
        return self.get_predicate(privileged=False)

    @property
    def predicate_privileged(self):
        return self.get_predicate(privileged=True)

    def __str__(self):
        return f"Role: {self.name}"

    def __repr__(self):
        return self.__str__()
