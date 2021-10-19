import rules
from django.contrib.auth.models import Group


class Role(Group):
    class Meta:
        proxy = True

    @classmethod
    def create(cls, **kwargs):
        parent = kwargs.pop('parent', None)
        obj, created = cls.objects.get_or_create(**kwargs)
        if not created:
            obj.parent = parent
        return obj

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    @property
    def predicate(self):
        predicate = rules.is_group_member(self.name)
        if self.parent:
            return predicate | self.parent.predicate
        return predicate
