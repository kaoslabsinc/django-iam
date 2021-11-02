import rules

p_system = rules.always_deny


class DefaultPerms:
    staff_readonly = {
        'add': p_system,
        'view': rules.is_staff,
        'change': p_system,
        'delete': p_system,
    }
