import rules

from iam.models import Role
from users.rules import Roles as UserRoles

rules.add_perm('blog', rules.is_staff)


class Roles:
    admin = Role.create(name="Blog Admin", parent=UserRoles.admin)
    author = Role.create(name="Blog Author", parent=admin)


is_blog_admin = Roles.admin.predicate
is_blog_author = Roles.author.predicate


@rules.predicate
def is_posts_author(user, post):
    return post and post.author == user
