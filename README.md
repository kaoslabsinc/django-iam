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
    simple_manager = Role('simple.SimpleManager')


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
from iam.mixins import IAMUserMixin


class User(
    IAMUserMixin,
    ...,
    AbstractUser
):
    ...
```

Now only users that have a `SimpleManager` profile can access `SimpleModel`.

For more examples, check out `example/blog`.

## Rationale

This package aims to improve upon the built-in Django authorization and permissions system, by making the system fully
programmatic and not rely on database objects like the built-in `Group` and `Permission` models. We believe access
governance in applications and projects should be evident form the code, and should not rely on database states and
migrations. An instance of an app deployed on a server should not have a different access governance structure than
another instance somewhere else (which can be the case using the Django built-in authorization system).

The excellent library [`django-rules`](https://github.com/dfunckt/django-rules) drastically improves upon the Django
permission system by enabling developers to create rule based systems similar to decision trees, without the need for
the database to be involved. It also allows devs to create object level permissions, something which the built-in
permission system doesn't allow.

`django-iam` builds on `django-rules` by introducing the concept of Roles and Profiles. In IAM each user is assigned one
or many roles, which determine their access to certain objects or paths in the application. Each Role has an associated
`Profile` which is a database model/object with a 1-1 relationship to the `User` model. A user has a Role if their User
account has the associated profile in an active state. Please check the [Quick Setup](#quick-setup) section for an
example on how to set IAM up in your Django project.

## Main tools

### Role (`iam.roles.Role`)

The main use of `Role` is to generate a predicate that checks whether a user has a certain profile or not:

```python
import rules
from rules.contrib.models import RulesModel
from iam.roles import Role

manager = Role('app.ManagerProfile')

is_manager = manager.predicate

rules.add_perm('app.change_model', is_manager)


class SomeModel(RulesModel):
    class Meta:
        rules_permissions = {
            'add': is_manager
        }


def some_view(request, pk):
    obj = get_object(pk)
    if is_manager.check(request.user, obj):  # checks if request.user has an active ManagerProfile or not
        ...
    else:
        ...
```

### AbstractProfileFactory (`iam.factories.AbstractProfileFactory`)

An [AbstractModelFactory](https://github.com/kaoslabsinc/django-building-blocks#abstract-model-factories)) to create
profiles. When you want to create a profile model, simply inherit from `AbstractProfileFactory.as_abstract_model()`. It
will create a one to one field to user on your profile model. You can also set options on `.as_abstract_model()` such
as:

```python
from iam.factories import AbstractProfileFactory

AbstractProfileFactory.as_abstract_model(related_name='manager_profiles')
AbstractProfileFactory.as_abstract_model(user_optional=True)  # To make the user field optional, useful to create
# profiles that won't be associated with a user account (e.g. a blog author that doesn't have an account on the system).
```

## Utilities

### Deactivating profiles

In order to delete/deactivate a role, just like the Django user model, do not delete the instance. Instead, you can
deactivate their profile by calling `instance.archive()`. Objects can be associated with Profile models, and you don't
want to delete them, lest your database state loses integrity (you already can't because of Django's deletion
protection). You can also deactivate a profile using the admin interface documented in the
following [section](#profileadmin).

```python
instance: ManagerProfile
instance.deactivate().save()  # To deactivate their profile and suspend their role
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
    fancy_manager = Role('fancy.FancyManager')


is_fancy_manager = Roles.fancy_manager.predicate

override_perms(GoodModel, {
    'view': is_fancy_manager,  # adding view permission to fancy_managers
})
```

For more examples, check out `example/simple2`.

## Optional tools and utilities (`iam.contrib`)

### `AbstractIAMUser`

`iam.contrib.users.models.AbstractIAMUser`

`django-iam` comes with two abstract user models to assist in your development. `AbstractBaseIAMUser` implements the
methods required to enable role-based permissions on the user and is the equivalent to django's `AbstractBaseUser`.
`AbstractIAMUser` implements role-based permissions, `RulesModel` to enable rule based permission on the User model
itself plus a number of properties such as `full_name`, `display_name`, and `initials`. Please refer to the code to see
what each method does.

### `IAMUserAdmin`

`iam.contrib.users.admin.IAMUserAdmin`

`IAMUserAdmin` is an enhancement over Django's default `UserAdmin`. It enables users to create staff users right from
the add user screen (important in certain workflows), hides superusers from non-superusers, and hides fields such as
user permissions from non-superusers, as they are neither useful in the IAM permissions model, nor every staff user
should have access to them.

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
