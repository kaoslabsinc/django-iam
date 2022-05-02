from iam.registry import get_registered_roles


class IAMUserMixin:
    def __init__(self, *args, **kwargs):
        self._roles = {}  # { ProfileModel: instance | False }
        super(IAMUserMixin, self).__init__(*args, **kwargs)

    @property
    def roles(self):
        return self._roles

    def set_role(self, model_cls):
        try:
            profile_instance = model_cls.objects.active().get(user=self)
        except model_cls.DoesNotExist:
            profile_instance = False
        self._roles[model_cls] = profile_instance
        return profile_instance

    def get_or_set_role(self, model_cls):
        profile_instance = self.roles.get(model_cls)  # None | False | instance
        if profile_instance is None:
            profile_instance = self.set_role(model_cls)
        return profile_instance

    def load_roles(self):
        self._roles = {}
        for model_cls in get_registered_roles():
            self.set_role(model_cls)
