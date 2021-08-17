import rules


def override_perms(cls, new_rules):
    for perm, rule in new_rules.items():
        rules.set_perm(cls.get_perm(perm), rule)
