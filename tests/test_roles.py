from blog.models import BlogAuthorProfile, BlogAdminProfile
from simple.models import SimpleAdminProfile
from users.models import AppAdminProfile


def test_load_roles(django_user_model):
    user = django_user_model.objects.create()
    app_admin_profile = AppAdminProfile.objects.create(user=user)
    blog_author_profile = BlogAuthorProfile.objects.create(user=user)

    user.load_roles()
    assert user.roles == {
        AppAdminProfile: app_admin_profile,
        BlogAdminProfile: False,
        SimpleAdminProfile: False,
        BlogAuthorProfile: blog_author_profile,
    }

    blog_author_profile.archive()
    blog_author_profile.save()
    user.load_roles()
    assert user.roles == {
        AppAdminProfile: app_admin_profile,
        BlogAdminProfile: False,
        SimpleAdminProfile: False,
        BlogAuthorProfile: False,
    }
