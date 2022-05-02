import rules

from iam.utils import lazy_get_predicate

rules.add_perm('simple', rules.is_staff)

is_simple_admin = lazy_get_predicate('simple.SimpleAdminProfile')
