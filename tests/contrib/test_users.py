from django.urls import reverse

from users.rules import Roles as UserRoles


def test_AbstractIAMUser(django_user_model):
    username = 'user'
    user = django_user_model.objects.create_user(username=username)
    assert user.full_name == ""
    assert user.display_name == username
    assert user.initials == "U"

    user.first_name = "User"
    user.last_name = "McUser"
    user.save()
    assert user.full_name == "User McUser"
    assert user.display_name == "User McUser"
    assert user.initials == "UM"


def test_IAMUserAdmin(client, django_user_model):
    default_user_post_dict = {
        'is_active': True,
        'is_staff': True,
    }
    user_superuser_username = 'user_superuser'
    user_superuser = django_user_model.objects.create(username=user_superuser_username, is_staff=True,
                                                      is_superuser=True)
    user_staff_username = 'user_staff'
    user_staff = django_user_model.objects.create(username=user_staff_username, is_staff=True)
    admin_group = UserRoles.admin.load_group()
    user_staff.groups.add(admin_group)

    opts = django_user_model._meta
    admin_url_changelist = reverse(f'admin:{opts.app_label}_{opts.model_name}_changelist')
    admin_url_change_superuser = reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[user_superuser.id])

    # Check if superuser can access change page for superusers
    client.force_login(user_superuser)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change_superuser)
    assert response.status_code == 200

    # Check is superuser can edit is_superuser, a protected attribute
    response = client.post(
        admin_url_change_superuser,
        {
            **default_user_post_dict,
            'username': user_superuser_username,
            'is_superuser': False,
        }
    )
    assert response.status_code == 302
    user_superuser.refresh_from_db()
    assert not user_superuser.is_superuser
    user_superuser.is_superuser = True  # Set this back to the original condition for the rest of the test
    user_superuser.save()

    # Check if normal staff can access change page for superusers
    client.force_login(user_staff)
    response = client.get(admin_url_changelist)
    assert response.status_code == 200
    response = client.get(admin_url_change_superuser)
    assert response.status_code == 302

    # Check if normal staff can edit is_superuser, a protected attribute
    admin_url_change_staff_user = reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[user_staff.id])
    response = client.post(
        admin_url_change_staff_user,
        {
            **default_user_post_dict,
            'username': user_staff_username,
            'is_superuser': True,
        }
    )
    assert response.status_code == 302
    user_staff.refresh_from_db()
    assert not user_staff.is_superuser
