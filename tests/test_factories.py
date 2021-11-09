from blog.models import BlogAuthorProfile, BlogPost


def test_owner_alias(django_user_model):
    user = django_user_model.objects.create()
    profile = BlogAuthorProfile.objects.create(user=user)
    post = BlogPost.objects.create(name="Name", owner=profile)
    assert post.owner == post.author
