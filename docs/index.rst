Welcome to Django Identity and Access Management's documentation!
*****************************************************************

Roles and access management for django apps

::

    pip install django-iam

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    tutorial
    advanced_tutorial
    modules
    contrib/index

.. contents:: On this page
    :local:
    :depth: 2

Rationale
=========
This package aims to improve upon the built-in Django authorization and permissions system, by making the system fully
programmatic and not rely on database objects like the built-in ``Group`` and ``Permission`` models. We believe access
governance in applications and projects should be evident form the code, and should not rely on database states and
migrations. An instance of an app deployed on a server should not have a different access governance structure than
another instance somewhere else (which can be the case using the Django built-in authorization system).

The excellent library `django-rules <django-rules>`_ drastically improves upon the Django permission system by enabling
developers to create rule based systems similar to decision trees, without the need for the database to be involved.
It also allows devs to create object level permissions, something which the built-in permission system doesn't allow.

django-iam builds on django-rules by introducing the concept of Roles and Profiles. In IAM each user is assigned one or
many `roles`, which determine their access to certain objects or paths in the application. Each `Role` has an associated
`Profile` which is a database model/object with a 1-1 relationship to the `User` model. A user has a Role if their User
account has the associated profile in an active/available state. Please check the :doc:`tutorial` section
for an example on how to set IAM up in your Django project.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
