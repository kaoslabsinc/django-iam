import rules


class Role:
    def __init__(self, name, parent: 'Role' = None):
        self.name = name
        self.parent = parent
        self._group = None

    @property
    def group(self):
        from django.contrib.auth.models import Group

        if self._group is None:
            self._group, _ = Group.objects.get_or_create(name=self.name)
        return self._group

    @property
    def predicate(self):
        predicate = rules.is_group_member(self.name)
        if self.parent:
            return predicate | self.parent.predicate
        return predicate
