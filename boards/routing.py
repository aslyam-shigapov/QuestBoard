"""
WebSocket-маршруты для приложения boards.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws/chat/<board_id>/ — чат конкретной доски
    re_path(r'^ws/chat/(?P<board_id>\d+)/$', consumers.BoardChatConsumer.as_asgi()),
]