# Django Identity and Access Management

Roles and access management for django apps

## Quick Setup

```shell
pip install django-iam
```

Make sure you have a custom user model setup and in `settings.py` you have

```python
AUTH_USER_MODEL = 'users.User'  # Point to your custom user model
```

Add the following to `INSTALLED_APPS` and `AUTHENTICATION_BACKENDS` settings
(refer to [django-rules docs](https://github.com/dfunckt/django-rules#readme))

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    ...,  # django apps

    'rules.apps.AutodiscoverRulesConfig',  # <-- add this after django apps, but before your own apps

    'users',
    ...
]

AUTHENTICATION_BACKENDS = [
    ...,
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    ...
]
```

Create a profile for the role, e.g.

```python
# app/models.py
from django.db import models
from iam.factories import AbstractProfileFactory


class SimpleManager(
    AbstractProfileFactory.as_abstract_model(related_name='simple_manager_profile'),
    models.Model
):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)  # comes from AbstractProfileFactory
    pass
```

In your app, create a `rules.py`:

```python
# app/rules.py
import rules

from iam.roles import Role

# refer to https://github.com/dfunckt/django-rules#permissions-in-the-admin for why this is here
rules.add_perm('app', rules.is_staff)


# django-iam code
class Roles:
    simple_manager = Role('simple_manager', 'simple.SimpleManager')


is_simple_manager = Roles.simple_manager.predicate
```

In your model that you are planning to set access to:

```python
# app/models.py
from rules.contrib.models import RulesModel
from app.rules import is_simple_manager


class SimpleModel(
    RulesModel
):
    name = models.CharField(max_length=100)

    class Meta:
        rules_permissions = {
            'add': is_simple_manager,
            'view': is_simple_manager,
            'change': is_simple_manager,
            'delete': is_simple_manager,
        }

```

As the last step, enable your user model to work with IAM and roles by having it inherit `RolesUserMixin`:

```python
# users/models.py
from iam.mixins import RolesUserMixin


class User(
    RolesUserMixin,
    ...,
    AbstractUser
):
    ...
```

Now only users that have a `SimpleManager` profile can access `SimpleModel`.

For more examples, check out `example/simple`.

## Utilities

### Deactivating profiles

In order to delete/deactivate a role, just like the Django user model, do not delete the instance. Instead, you can
deactivate their profile by calling `instance.archive()`. Objects can be associated with Profile models, and you don't
want to delete them, lest your database state loses integrity (you already can't because of Django's deletion
protection). You can also deactivate a profile using the admin interface documented in the
following [section](#profileadmin).

```python
instance: ManagerProfile
instance.archive().save()  # To deactivate their profile and suspend their role
instance.restore().save()  # To activate their profile and restore their role
```

### `ProfileAdmin`

For the best experience in the admin interface with profile models, have your profile admins inherit
form `iam.admin.admin.ProfileAdmin`. This enables autocomplete on the user field, and also allows you to activate and
deactivate profiles with a click. In order to use `ProfileAdmin`, add `django_object_actions` to your `INSTALLED_APPS`.
`django-object-actions` (already installed as a dependency) allows object level actions in the admin interface.

```python
# settings.py
INSTALLED_APPS = [
    ...,
    'django_object_actions',
    ...
]

# admin.py
from iam.admin.admin import ProfileAdmin


@admin.register(ManagerProfile)
class ManagerProfileAdmin(ProfileAdmin):
    ...
```

### Override permissions

This utility is useful when you install an app that has access permissions set up using `iam` and you are looking to
override its settings.

Say you want to `outside_app.GoodModel` permissions to be readable by the `fancy_manager` role. The `fancy_manager` role
is defined in the `fancy` app:

```python
# settings.py 
INSTALLED_APPS = [
    ...,
    'outside_app',
    ...,
    'fancy',  # needs to be installed after `outside_app`
]

# fancy/rules.py
from iam.utils import override_perms
from iam.roles import Role
from outside_app.models import GoodModel


class Roles:
    fancy_manager = Role('fancy_manager', 'fancy.FancyManager')


is_fancy_manager = Roles.fancy_manager.predicate

override_perms(GoodModel, {
    'view': is_fancy_manager,  # adding view permission to fancy_managers
})
```

For more examples, check out `example/simple2`.

### `HasOwnerFactory`

A common design pattern is to associate instances of objects with a user. For example, a blog post might have an author
which can also give them extra permissions to that blog post since they are the author/owner of that object. Using IAM,
instead of associating the object with the user model directly, you associate the object with the profile. In the blog
post example, the `BlogPost` model would have a foreign key to the `BlogAuthor` model.

IAM comes with an abstract model factory (to read more about abstract model factories,
check [`django-building-blocks`](https://github.com/kaoslabsinc/django-building-blocks)) to facilitate this design
pattern. In the blog post example:

```python
from iam.factories import HasOwnerFactory


class BlogPost(
    HasOwnerFactory.as_abstract_model(BlogAuthor),
    models.Model
):
    ...
```

Now your `BlogPost` model has a foreign key to `BlogAuthor`.

## Development and Testing

### IDE Setup

Add the `example` directory to the `PYTHONPATH` in your IDE to avoid seeing import warnings in the `tests` modules. If
you are using PyCharm, this is already set up.

### Running the Tests

Install requirements

```
pip install -r requirements.txt
```

For local environment

```
pytest
```

For all supported environments

```
tox
```
