
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json

class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print(f"Closed with code: {close_code}")
        self.close()

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'message': text_data
        }))


class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from client: {data}")
        # Process the incoming data (could be an event)

        # Send a message back to the client
        await self.send(text_data=json.dumps({
            'command': 'Some command or response'
        }))

    async def send_command(self, event):
        # This method can be called from elsewhere in your Django application
        await self.send(text_data=json.dumps({
            'command': event['command']
        }))