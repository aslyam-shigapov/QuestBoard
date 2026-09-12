from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Board
from .serializers import BoardSerializer


@extend_schema(
    tags=['Boards'],
    summary='Список публичных досок',
    description='Возвращает список всех публичных досок.',
)
class BoardListAPIView(generics.ListAPIView):
    """GET /api/boards/ — список публичных досок."""
    serializer_class = BoardSerializer
    queryset = Board.objects.filter(is_public=True)
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=['Boards'],
    summary='Детали доски',
    description='Возвращает одну доску по ID.',
)
class BoardDetailAPIView(generics.RetrieveAPIView):
    """GET /api/boards/<id>/ — детали доски."""
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = 'board_id'