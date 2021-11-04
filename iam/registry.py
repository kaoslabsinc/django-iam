class RolesRegistry:
    def __init__(self):
        self.registered_roles_dict = {}

    def register(self, model_cls=None, **conf):
        def wrapper(m_cls):
            self.registered_roles_dict[m_cls] = {**conf}
            return m_cls

        if model_cls is None:
            return wrapper
        else:
            return wrapper(model_cls)

    def get_registered_roles(self, filter_func=lambda conf: True):
        return set(model_cls
                   for model_cls, conf in self.registered_roles_dict.items()
                   if filter_func(conf))


registry = RolesRegistry()
register_role = registry.register
get_registered_roles = registry.get_registered_roles
