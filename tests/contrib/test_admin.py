from django.urls import reverse

from blog.models import BlogAuthorProfile, BlogPost
from users.models import AppAdminProfile


def test_ProfileAdmin(client, django_user_model):
    opts = BlogAuthorProfile._meta
    admin_url_changelist = reverse(f'admin:{opts.app_label}_{opts.model_name}_changelist')

    user = django_user_model.objects.create(username='user', is_staff=True)
    profile = BlogAuthorProfile.objects.create(user=user)

    superuser = django_user_model.objects.create(username='superuser', is_staff=True, is_superuser=True)
    client.force_login(superuser)
    client.post(admin_url_changelist,
                {'action': 'archive', '_selected_action': [profile.id]})

    profile.refresh_from_db()
    assert not profile.is_active


def test_AutoOwnerAdminMixin(client, django_user_model):
    opts = BlogPost._meta
    admin_url_add = reverse(f'admin:{opts.app_label}_{opts.model_name}_add')

    user = django_user_model.objects.create(username='user', is_staff=True)
    BlogAuthorProfile.objects.create(user=user)
    client.force_login(user)
    response = client.get(
        admin_url_add,
    )
    assert response.context_data['adminform'].form.fields['owner'].initial.user == user

    user2 = django_user_model.objects.create(username='user2', is_staff=True)
    AppAdminProfile.objects.create(user=user2)
    client.force_login(user2)
    response = client.get(
        admin_url_add,
    )
    assert response.context_data['adminform'].form.fields['owner'].initial is None
