import rules

from iam.utils import lazy_get_predicate

rules.add_perm('simple', rules.is_staff)

is_author = lazy_get_predicate('simple.AuthorProfile')
is_super_author = lazy_get_predicate('simple.AuthorProfile', lambda p: p.is_super_author)
