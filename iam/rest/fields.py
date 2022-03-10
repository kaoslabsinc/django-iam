from rest_framework import serializers

__all__ = [
    'CurrentProfileDefault',
]


class CurrentProfileDefault(serializers.CurrentUserDefault):
    def __init__(self, profile_cls, create=False):
        self.profile_cls = profile_cls
        self.create = create

    def __call__(self, serializer_field):
        user = super(CurrentProfileDefault, self).__call__(serializer_field)
        if not user.is_authenticated:
            return None

        try:
            return self.profile_cls.objects.get(user=user)
        except self.profile_cls.DoesNotExist:
            if self.create:
                return self.profile_cls.objects.create(user=user)
            else:
                return None
