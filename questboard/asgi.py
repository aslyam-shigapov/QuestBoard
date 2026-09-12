"""
ASGI config for questboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questboard.settings')

# Сначала инициализируем Django ASGI приложение
django_asgi_app = get_asgi_application()

# Импортируем routing ПОСЛЕ get_asgi_application()
from boards.routing import websocket_urlpatterns  # noqa

application = ProtocolTypeRouter({
    # Все HTTP-запросы — в обычный Django
    'http': django_asgi_app,

    # WebSocket — через AuthMiddlewareStack (для request.user)
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})