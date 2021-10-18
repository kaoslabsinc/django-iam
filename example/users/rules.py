import rules

from iam.roles import Role

rules.add_perm('users', rules.is_staff)


class Roles:
    admin = Role("Admin")


is_admin = Roles.admin.predicate
