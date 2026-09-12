from rest_framework import serializers
from .models import Quest, QuestCompletion


class QuestSerializer(serializers.ModelSerializer):
    """Сериализатор квеста."""
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Quest
        fields = [
            'id', 'board', 'title', 'description',
            'xp_reward', 'difficulty', 'difficulty_display', 'is_active',
        ]


class QuestCompletionSerializer(serializers.ModelSerializer):
    """Сериализатор выполнения квеста."""
    quest_title = serializers.CharField(source='quest.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = QuestCompletion
        fields = ['id', 'quest', 'quest_title', 'user', 'user_username', 'completed_at']
        read_only_fields = ['user', 'completed_at']