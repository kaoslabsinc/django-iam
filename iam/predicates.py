import rules


@rules.predicate
def is_owner(user, obj):
    return obj is None or obj.owner.user == user


@rules.predicate
def is_user(user, obj):
    return obj is None or obj.user == user
