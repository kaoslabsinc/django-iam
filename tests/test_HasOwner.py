from django.urls import reverse

from blog.models import BlogAuthor, BlogPost, BlogManager


def test_HasOwnerAdmin(client, django_user_model):
    user_manager = django_user_model.objects.create(username='user_manager', is_staff=True)
    user_owner = django_user_model.objects.create(username='user_owner', is_staff=True)
    user_non_owner = django_user_model.objects.create(username='user_non_owner', is_staff=True)

    BlogManager.objects.create(user=user_manager)
    owner_profile = BlogAuthor.objects.create(user=user_owner)
    BlogAuthor.objects.create(user=user_non_owner)

    opts = BlogPost._meta
    obj = BlogPost.objects.create(owner=owner_profile)
    admin_url_changelist = reverse(f'admin:{opts.app_label}_{opts.model_name}_changelist')
    admin_url_change = reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.id])

    client.force_login(user_manager)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 200

    client.force_login(user_owner)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 200

    client.force_login(user_non_owner)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 403
