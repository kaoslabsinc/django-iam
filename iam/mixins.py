class IAMUserMixin:
    def __init__(self, *args, **kwargs):
        self._roles = {}
        super(IAMUserMixin, self).__init__(*args, **kwargs)

    def load_roles(self):
        raise NotImplementedError

    def set_role(self, model_class, instance):
        self._roles[model_class] = instance

    @property
    def roles(self):
        return self._roles
