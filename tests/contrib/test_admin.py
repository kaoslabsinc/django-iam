from django.urls import reverse

from blog.models import BlogAuthorProfile, BlogPost


def test_AutoOwnerAdminMixin(client, django_user_model):
    user = django_user_model.objects.create(is_staff=True)
    BlogAuthorProfile.objects.create(user=user)

    opts = BlogPost._meta
    admin_url_add = reverse(f'admin:{opts.app_label}_{opts.model_name}_add')

    client.force_login(user)
    response = client.get(
        admin_url_add,
    )

    assert response.context_data['adminform'].form.fields['owner'].initial.user == user
