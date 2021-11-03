import rules

from iam.utils import lazy_get_predicate

rules.add_perm('blog', rules.is_staff)

is_blog_admin = lazy_get_predicate('blog.BlogAdminProfile')
