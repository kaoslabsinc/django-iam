class RolesRegistry:
    def __init__(self):
        self.registered_roles_dict = {}

    def register(self, model_cls=None, admin=False):
        def wrapper(m_cls):
            self.registered_roles_dict[m_cls] = {
                'admin': admin
            }
            return m_cls

        if model_cls is None:
            return wrapper
        else:
            return wrapper(model_cls)

    @property
    def registered_roles(self):
        return set(self.registered_roles_dict.keys())


registry = RolesRegistry()
register_role = registry.register
registered_roles = registry.registered_roles
