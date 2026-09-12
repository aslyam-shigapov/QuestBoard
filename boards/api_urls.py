from django.urls import path
from .api import BoardListAPIView, BoardDetailAPIView

app_name = 'boards_api'

urlpatterns = [
    path('', BoardListAPIView.as_view(), name='list'),
    path('<int:board_id>/', BoardDetailAPIView.as_view(), name='detail'),
]