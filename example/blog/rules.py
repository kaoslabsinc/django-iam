import rules

from iam.utils import lazy_get_predicate

rules.add_perm('blog', rules.is_staff)

is_blog_admin = lazy_get_predicate('blog.BlogAdminProfile')
is_blog_author = lazy_get_predicate('blog.BlogAuthorProfile')


@rules.predicate
def is_privileged_blog_author(user):
    from .models import BlogAuthorProfile
    return BlogAuthorProfile.check_user(lambda profile: profile.is_privileged)(user)
