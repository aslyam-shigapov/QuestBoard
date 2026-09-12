from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    """Сериализатор доски."""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    quests_count = serializers.IntegerField(source='quests.count', read_only=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description', 'cover',
            'is_public', 'created_at',
            'owner', 'owner_username', 'quests_count',
        ]
        read_only_fields = ['owner', 'created_at']