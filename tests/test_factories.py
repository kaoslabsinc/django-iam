from blog.models import BlogAuthorProfile, BlogPost


def test_owner_alias(django_user_model):  # TODO: test where owner_alias doesn't exist, default case
    user = django_user_model.objects.create()
    profile = BlogAuthorProfile.objects.create(user=user)
    post = BlogPost.objects.create(name="Name", owner=profile)
    assert post.owner == post.author
