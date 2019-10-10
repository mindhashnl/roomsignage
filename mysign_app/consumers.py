import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ScreenConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # Link to group of door device id
        screen_id = self.scope["url_route"]["kwargs"]["screen_id"]
        async_to_sync(self.channel_layer.group_add)(screen_id, self.channel_name)

    def disconnect(self, close_code):
        # Disconnect from group
        screen_id = self.scope["url_route"]["kwargs"]["screen_id"]
        async_to_sync(self.channel_layer.group_discard)(screen_id, self.channel_name)

    def message(self, data):
        # Forward the messages
        self.send(text_data=json.dumps(data))
