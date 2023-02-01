Modules
*******

.. contents::
    :depth: 2
    :local:


Models
======
.. automodule:: iam.models

.. autoclass:: UserProfileModel
    :members: get_for_user

Registry
========
.. automodule:: iam.registry

.. autoclass:: RolesRegistry

.. py:function:: register_role

    Decorator to register a profile model as a role in the application

    :param model_cls: The profile model class. Passed through the decorator
    :param conf: optional configuration, attributes and tags for the role to be registered.
    :return: `model_cls`

.. py:function:: get_registered_roles

    Return a set off all registered profile model classes

    :param filter_func: Optionally pass in a function that takes a profile class as an argument, and returns True
        or False depending on whether the class should be included in the return value or not.
    :return: Set off all registered profile model classes, optionally filtered by `filter_func` logic.


Mixins
========
.. automodule:: iam.mixins

.. autoclass:: RolePredicateMixin
    :members:

.. autoclass:: IAMUserMixin
    :members:


Predicates
===========
.. automodule:: iam.predicates

.. autofunction:: is_owner
.. autofunction:: is_user


Utils
===========
.. automodule:: iam.utils
    :members:
