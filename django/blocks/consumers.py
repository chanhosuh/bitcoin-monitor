import json

from django.core.cache import cache

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BlockConsumer(WebsocketConsumer):
    def connect(self):
        """
        open websocket and send first update
        """
        # route_kwargs = self.scope['url_route']]['kwargs']
        self.topic = "block"
        async_to_sync(self.channel_layer.group_add)(
            self.topic, self.channel_name,
        )
        super().connect()
        self.send(text_data=json.dumps({"message": f"connected"}))
        self.block_update({"block": cache.get(self.topic)})

    def disconnect(self, close_code):
        """ leave group and disconnect """
        async_to_sync(self.channel_layer.group_discard)(
            self.message_type, self.channel_name
        )
        super().disconnect(close_code)

    def block_update(self, event):
        """ extract block from event and send to websocket """
        block = event["block"]
        self.send(text_data=json.dumps({"block": block,}))
