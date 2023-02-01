Get Started
***********

.. highlight:: bash

Install::

    pip install django-iam

.. highlight:: python

Make sure you have a custom user model setup and in ``settings.py`` you have::

    AUTH_USER_MODEL = 'users.User'  # Point to your custom user model

Add iam to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        ...,  # django apps
        'iam',
        ...,  # Your apps
    ]

Since django-iam is based on `django-rules <https://github.com/dfunckt/django-rules>`_, add
``rules.permissions.ObjectPermissionBackend`` to your authentication backends::

    AUTHENTICATION_BACKENDS = [
        ...,
        'rules.permissions.ObjectPermissionBackend',  # <-- This one
        'django.contrib.auth.backends.ModelBackend',
        ...
    ]

Enable your user model to work with IAM and roles by having it inherit ``IAMUserMixin``::

    # users/models.py
    from iam.mixins import IAMUserMixin

    class User(
        IAMUserMixin,
        ...,
        AbstractUser
    ):
        ...

Now you can create a profile model for a role::

    # some_app/models.py
    from django.db import models
    from iam.models import UserProfileModel
    from iam.registry import register_role
    from iam.contrib.utils import get_profile_cls_verbose_name_plural


    @register_role
    class SomeRoleProfile(
        UserProfileModel,
        models.Model
    ):
        # comes from UserProfileModel, feel free to override it to set `related_name` or make it optional and nullable
        # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

        class Meta:
            # Adds a little 👤 emoji to the name in admin, to make it clear this is a profile model
            verbose_name_plural = get_profile_cls_verbose_name_plural('BlogAdminProfile')

In your app, create a rules.py::

    # some_app/rules.py
    import rules
    from iam.utils import lazy_get_predicate

    # refer to https://github.com/dfunckt/django-rules#permissions-in-the-admin for why this is here
    rules.add_perm('some_app', rules.is_staff)

    is_some_role = lazy_get_predicate('some_app.SomeRoleProfile')

In the model that you are planning to set access to::

    # app/models.py
    from rules.contrib.models import RulesModel
    from some_app.rules import is_some_role


    class SomeModel(
        RulesModel
    ):
        name = models.CharField(max_length=100)

        class Meta:
            rules_permissions = {
                'add': is_some_role,
                'view': is_some_role,
                'change': is_some_role,
                'delete': is_some_role,
            }

Now only users that have a ``SomeRoleProfile`` profile can access ``SomeModel``.

For more examples, check out `example/blog`.

