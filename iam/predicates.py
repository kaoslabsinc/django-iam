import rules


@rules.predicate
def is_owner(user, obj):
    """
    Rules predicate to determine whether a user is the owner of an object or not.
    """
    return obj is None or obj.owner.user == user


@rules.predicate
def is_user(user, obj):
    """
    Rules predicate to determine whether a profile belongs to a user or not.
    """
    return obj is None or obj.user == user
