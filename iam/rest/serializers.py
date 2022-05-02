from rest_framework import serializers

__all__ = [
    'BaseProfileSerializer',
]


class BaseProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = (
            'user',
        )
