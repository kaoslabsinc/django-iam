import rules

from iam.roles import Role

rules.add_perm('simple', rules.is_staff)


class Roles:
    simple_manager = Role('simple_manager', 'simple.SimpleManager')


is_simple_manager = Roles.simple_manager.predicate
