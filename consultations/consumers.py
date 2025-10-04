from channels.generic.websocket import AsyncJsonWebsocketConsumer

class SignalingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # content: {type: "offer"/"answer"/"candidate", data: ... , sender: "doctor"/"patient"}
        await self.channel_layer.group_send(self.room_id, {
            "type": "signal.message",
            "message": content
        })

    async def signal_message(self, event):
        await self.send_json(event["message"])