from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'xp', 'level', 'avatar', 'bio']
        read_only_fields = ['user', 'xp', 'level']