from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Quest
from .serializers import QuestSerializer


@extend_schema(
    tags=['Quests'],
    summary='Список квестов',
    description='Список активных квестов. Фильтр по доске: ?board=<id>.',
)
class QuestListAPIView(generics.ListAPIView):
    """GET /api/quests/?board=<id> — список квестов."""
    serializer_class = QuestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Quest.objects.filter(is_active=True)
        board_id = self.request.query_params.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset