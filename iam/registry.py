ADMIN = 'admin'


class RolesRegistry:
    def __init__(self):
        self.registered_roles_dict = {}

    def register(self, model_cls=None, admin=False):
        def wrapper(m_cls):
            self.registered_roles_dict[m_cls] = {
                ADMIN: admin
            }
            return m_cls

        if model_cls is None:
            return wrapper
        else:
            return wrapper(model_cls)

    def get_registered_roles(self):
        return set(self.registered_roles_dict.keys())

    def get_admin_roles(self):
        return set(k for k, v in self.registered_roles_dict.items() if v[ADMIN])


registry = RolesRegistry()
register_role = registry.register
get_registered_roles = registry.get_registered_roles
get_admin_roles = registry.get_admin_roles
