import rules

from iam.models import Role

rules.add_perm('users', rules.is_staff)


class Roles:
    admin = Role.create(name="Admin")


is_admin = Roles.admin.predicate
