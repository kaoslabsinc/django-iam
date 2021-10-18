from django.contrib.auth.models import Group
from django.urls import reverse

from blog.models import BlogPost
from blog.rules import Roles as BlogRoles
from users.rules import Roles as UserRoles


def test_BlogPostAccess(client, django_user_model):
    user_admin = django_user_model.objects.create(username='user_admin', is_staff=True)
    user_author_owner = django_user_model.objects.create(username='user_author_owner', is_staff=True)
    user_author_non_owner = django_user_model.objects.create(username='user_author_non_owner', is_staff=True)
    user_staff = django_user_model.objects.create(username='user_staff', is_staff=True)

    admin_group = UserRoles.admin.group
    # admin_group = Group.objects.get(name=UserRoles.admin.name)
    author_group = BlogRoles.author.group
    user_admin.groups.add(admin_group)
    author_group.user_set.add(user_author_owner, user_author_non_owner)

    opts = BlogPost._meta
    obj = BlogPost.objects.create(author=user_author_owner)
    admin_url_changelist = reverse(f'admin:{opts.app_label}_{opts.model_name}_changelist')
    admin_url_change = reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.id])

    client.force_login(user_admin)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 200

    client.force_login(user_author_owner)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 200

    client.force_login(user_author_non_owner)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change)
    assert response.status_code == 200

    client.force_login(user_staff)
    response = client.get(admin_url_changelist)
    assert response.status_code == 403
    response = client.get(admin_url_change)
    assert response.status_code == 403
