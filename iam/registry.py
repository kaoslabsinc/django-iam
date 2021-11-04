class RolesRegistry:
    def __init__(self):
        self.registered_roles = set()

    def register(self, model):
        self.registered_roles.add(model)
        return model


registry = RolesRegistry()
register_role = registry.register
registered_roles = registry.registered_roles
