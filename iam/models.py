import rules
from django.contrib.auth.models import Group


class Role(Group):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def upgrade_from_db(self):
        group, _ = Group.objects.get_or_create(name=self.name)
        self.id = group.id
        self.refresh_from_db()

    @property
    def predicate(self):
        predicate = rules.is_group_member(self.name)
        if self.parent:
            return predicate | self.parent.predicate
        return predicate
