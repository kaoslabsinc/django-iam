import pytest


def has_perm(model_cls, perm, user, obj=None):
    perm = model_cls.get_perm(perm)
    return user.has_perm(perm, obj) if obj else user.has_perm(perm)


def assert_has_perm_bulk(model_cls, user, obj, perms):
    for perm, conf in perms.items():
        access_all, access_obj = conf
        if access_all is not None and has_perm(model_cls, perm, user) != access_all:
            if access_all:
                message = f"{user} doesn't have {perm} permissions on {model_cls}, but it should"
            else:
                message = f"{user} has {perm} permissions on {model_cls}, but it shouldn't"
            pytest.fail(message)
        if access_obj is not None and has_perm(model_cls, perm, user, obj) != access_obj:
            if access_obj:
                message = f"{user} doesn't have {perm} permissions on {obj}, but it should"
            else:
                message = f"{user} has {perm} permissions on {obj}, but it shouldn't"
            pytest.fail(message)
