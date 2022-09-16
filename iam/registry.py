from typing import Callable, Any


class RolesRegistry:
    """
    A central registry to keep track of all different roles in the application.
    Register your profile models with @register decorator.
    """

    def __init__(self):
        self.registered_roles_dict = {}

    def register(self, model_cls=None, **conf):
        """
        Decorator to register a profile model as a role in the application

        :param model_cls: The profile model class. Passed through the decorator
        :param conf: optional configuration, attributes and tags for the role to be registered.
        :return: `model_cls`
        """

        def wrapper(m_cls):
            self.registered_roles_dict[m_cls] = {**conf}
            return m_cls

        if model_cls is None:
            return wrapper
        else:
            return wrapper(model_cls)

    def get_registered_roles(self, filter_func: Callable[[Any], bool] = None) -> set:
        """
        Return a set off all registered profile model classes

        :param filter_func: Optionally pass in a function that takes a profile class as an argument, and returns True
            or False depending on whether the class should be included in the return value or not.
        :return: Set off all registered profile model classes, optionally filtered by `filter_func` logic.
        """
        return set(model_cls
                   for model_cls, conf in self.registered_roles_dict.items()
                   if not filter_func or filter_func(conf))


registry = RolesRegistry()
register_role = registry.register
get_registered_roles = registry.get_registered_roles
