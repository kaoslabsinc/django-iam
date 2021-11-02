import rules
from django.contrib.auth.models import Group


class Role(Group):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def refresh_from_db(self, using=None, fields=None):
        if not self.id:
            group = Group.objects.get(name=self.name)
            self.id = group.id
        super().refresh_from_db(using=using, fields=fields)

    @property
    def predicate(self):
        predicate = rules.is_group_member(self.name)
        if self.parent:
            return predicate | self.parent.predicate
        return predicate
