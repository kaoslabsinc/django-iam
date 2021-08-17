from simple.models import SimpleManager, SimpleModel


def test_model_access(django_user_model):
    user_has_access = django_user_model.objects.create(username='user_has_access')
    user_has_no_access = django_user_model.objects.create(username='user_has_no_access')

    SimpleManager.objects.create(user=user_has_access)

    add_model_perm = SimpleModel.get_perm('add')
    assert user_has_access.has_perm(add_model_perm)
    assert not user_has_no_access.has_perm(add_model_perm)
