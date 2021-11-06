from django.urls import reverse

from blog.models import BlogAuthorProfile, BlogPost
from users.models import AppAdminProfile


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
