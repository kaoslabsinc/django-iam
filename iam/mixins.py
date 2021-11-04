from iam.registry import registered_roles


class IAMUserMixin:
    def __init__(self, *args, **kwargs):
        self._roles = {}  # { ProfileModel: instance | False }
        super(IAMUserMixin, self).__init__(*args, **kwargs)

    def load_roles(self):
        self._roles = {}
        for model_cls in registered_roles:
            try:
                instance = model_cls.objects.active().get(user=self)
            except model_cls.DoesNotExist:
                instance = False
            self.set_role(model_cls, instance)

    def set_role(self, model_class, instance):
        self._roles[model_class] = instance

    @property
    def roles(self):
        return self._roles
