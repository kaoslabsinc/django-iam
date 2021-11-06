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

Add `iam` to your `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    ...,  # django apps
    'iam',
    ...,  # Your apps
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
from iam.contrib.utils import get_profile_class_verbose_name_plural


class SomeRoleProfile(
    AbstractProfileFactory.as_abstract_model(related_name='blog_author_profile'),
    models.Model
):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)  # comes from AbstractProfileFactory

    class Meta:
        # Adds a little 👤 emoji to the name in admin, to make it clear this is a profile model
        verbose_name_plural = get_profile_class_verbose_name_plural('BlogAdminProfile')
```

In your app, create a `rules.py`:

```python
# app/rules.py
import rules
from iam.utils import lazy_get_predicate

# refer to https://github.com/dfunckt/django-rules#permissions-in-the-admin for why this is here
rules.add_perm('some_app', rules.is_staff)

is_some_role = lazy_get_predicate('some_app.SomeRole')
```

In your model that you are planning to set access to:

```python
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
```

As the last step, enable your user model to work with IAM and roles by having it inherit `IAMUserMixin`:

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

Now only users that have a `SomeRoleProfile` profile can access `SomeModel`.

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

### registry

### AbstractProfileFactory (`iam.factories.AbstractProfileFactory`)

### `lazy_get_predicate`

### Deactivating profiles

### predicates

### `HasOwnerFactory`

### Override permissions

## Optional tools and utilities (`iam.contrib`)

### `ProfileAdmin`

### `AutoOwnerAdminMixin`

### Admin roles

### `AbstractIAMUser`

### `IAMUserAdmin`

### `get_profile_class_verbose_name_plural`

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
