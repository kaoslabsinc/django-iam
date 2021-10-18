import rules

from iam.roles import Role

rules.add_perm('blog', rules.is_staff)


class Roles:
    blog_manager = Role('blog.BlogManager')
    blog_author = Role('blog.BlogAuthor')


is_blog_manager = Roles.blog_manager.predicate
is_blog_author = Roles.blog_author.predicate
