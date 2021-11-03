class RolesRegistry:
    def __init__(self):
        self.registered_roles = set()

    def register(self, *models):
        def wrapper():
            self.registered_roles.add(models)

        return wrapper


registry = RolesRegistry()
register_role = registry.register
