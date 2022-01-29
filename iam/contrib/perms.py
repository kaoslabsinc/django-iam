import rules


class Perms:
    all_is_staff = {
        'add': rules.is_staff,
        'change': rules.is_staff,
        'view': rules.is_staff,
        'delete': rules.is_staff,
    }
