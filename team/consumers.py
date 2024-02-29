from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
from . import models
import json


class OlineStatusConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        user = self.scope['user']
        self.update_user_status(user, 'online')

    async def websocket_receive(self, event):
        pass

    async def websocket_disconnect(self, event):
        user = self.scope['user']
        self.update_user_status(user, 'offline')

    @database_sync_to_async
    def update_user_status(self, user, status):
        return models.Employee.objects.filter(pk=user.pk).update(status=status)
