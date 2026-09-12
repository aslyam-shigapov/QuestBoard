"""
ASGI config for questboard project.
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questboard.settings')

# Сначала инициализируем Django
django_asgi_app = get_asgi_application()

# Импорт routing — ПОСЛЕ get_asgi_application()
from boards.routing import websocket_urlpatterns  # noqa
from django.conf import settings  # noqa
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler  # noqa


# Применяем обёртку для раздачи статики
if settings.DEBUG:
    django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})