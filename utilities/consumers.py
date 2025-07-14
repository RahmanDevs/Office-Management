from channels.generic.websocket import AsyncWebsocketConsumer
import json

# class ProgressConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'conversion_progress'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def send_progress(self, event):
#         await self.send(text_data=json.dumps({
#             'progress': event['progress'],
#             'message': event['message'],
#         }))


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=f"Echo: {text_data}")

    async def disconnect(self, close_code):
        pass