"""
WebSocket-обработчики (consumers) для досок QuestBoard.

Каждая доска — отдельная «комната». Сообщения одной комнаты
не видны в другой.
"""

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class BoardChatConsumer(WebsocketConsumer):
    """
    Чат доски. Комната = доска (по board_id).
    """

    def connect(self):
        # Имя комнаты берём из URL
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.room_group_name = f'board_{self.board_id}'

        # Подписываемся на группу
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

        # Проверяем пользователя
        user = self.scope.get('user')
        name = user.username if user and user.is_authenticated else 'Аноним'

        # Приветствие лично этому клиенту
        self.send(text_data=json.dumps({
            'message': f'💬 Добро пожаловать в чат доски #{self.board_id}, {name}!'
        }))

    def disconnect(self, close_code):
        # Отписываемся от группы
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        """Получили сообщение от одного клиента — рассылаем всем в комнате."""
        if text_data is None:
            return

        data = json.loads(text_data)
        message = data.get('message', '').strip()
        if not message:
            return

        user = self.scope.get('user')
        name = user.username if user and user.is_authenticated else 'Аноним'

        # Отправляем во ВСЮ группу
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # вызовет метод chat_message у всех
                'message': message,
                'sender': name,
            },
        )

    def chat_message(self, event):
        """Вызывается у ВСЕХ участников группы."""
        self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))