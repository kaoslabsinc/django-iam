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


class SimpleManager(
    models.Model
):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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
