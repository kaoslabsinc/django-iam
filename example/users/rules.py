import rules

from iam.utils import lazy_get_predicate

rules.add_perm('users', rules.is_staff)

is_admin = lazy_get_predicate('users.AppAdminProfile')
