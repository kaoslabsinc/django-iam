from simple.models import SimpleManager, SimpleModel, SimpleProxy


def test_model_access(django_user_model):
    user_has_access = django_user_model.objects.create(username='user_has_access')
    user_has_no_access = django_user_model.objects.create(username='user_has_no_access')

    SimpleManager.objects.create(user=user_has_access)

    add_model_perm = SimpleModel.get_perm('add')
    assert user_has_access.has_perm(add_model_perm)
    assert not user_has_no_access.has_perm(add_model_perm)


def test_model_overridden_access(django_user_model):
    user_has_access = django_user_model.objects.create(username='user_has_access')
    user_has_no_access = django_user_model.objects.create(username='user_has_no_access')

    SimpleManager.objects.create(user=user_has_access)

    add_model_perm = SimpleProxy.get_perm('add')
    assert not user_has_access.has_perm(add_model_perm)
    assert not user_has_no_access.has_perm(add_model_perm)

    view_model_perm = SimpleProxy.get_perm('view')
    assert user_has_access.has_perm(view_model_perm)
    assert not user_has_no_access.has_perm(view_model_perm)


def test_model_access_archived_profile(django_user_model):
    username = 'user'
    user = django_user_model.objects.create(username=username)
    profile = SimpleManager.objects.create(user=user)
    add_model_perm = SimpleModel.get_perm('add')
    assert user.has_perm(add_model_perm)

    profile.archive().save()
    user = django_user_model.objects.get(username=username)  # to reset _roles_cache
    assert not user.has_perm(add_model_perm)

    profile.restore().save()
    user = django_user_model.objects.get(username=username)
    assert user.has_perm(add_model_perm)
