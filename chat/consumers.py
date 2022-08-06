from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from . import models

import json
import re


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # O usuário da sessão
        self.user = self.scope['user']

        # O ID do outro usuário do chat
        self.friend_id = self.scope['url_route']['kwargs']['friend_id']

        # O nome da sala que será criada no channel
        self.room_group_name = "chat_room_%s" % self.friend_id

        # Criando o grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # O channel em que o grupo será adicionado
        )

        await self.accept()

    async def disconnect(self, code):
        #  Desconectando do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, bytes_data=None):
        json_data = json.loads(text_data)
        message = json_data.get('message')
        message = re.sub(r'<[^>]+?>', '', message)  # Remove as tag HTML das mensagens

        # Enviando mensagem para o grupo que foi criado
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # O tipo de mensagem
                # (Se for personalizada, será nescessário criar uma função que
                # receberá esse objeto)
                'type': 'chat_message',
                'message': message,
                'user': self.user.username
            }
        )

    async def chat_message(self, event):
        # Enviará a mensagem em formato JSON
        await self.send(text_data=json.dumps(event))
