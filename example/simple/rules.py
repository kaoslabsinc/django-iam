import rules

from iam.utils import lazy_get_predicate

rules.add_perm('liquidity_rewards', rules.is_staff)

is_author = lazy_get_predicate('simple.AuthorProfile')
