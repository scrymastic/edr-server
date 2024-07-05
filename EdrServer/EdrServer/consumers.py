
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
from utils.agent_item import AgentItem
from utils.event_manager import EventManager


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connected to client")


    def disconnect(self, close_code):
        print(f"Closed with code: {close_code}")
        self.close()


    def receive(self, text_data):
        print(f"Received from client: {text_data}")
        self.send(text_data=json.dumps({
            'type': 'echo',
            'message': str(text_data)
        }))



class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.agent_ip = self.scope['client'][0]
        await self.channel_layer.group_add(self.agent_ip, self.channel_name)
        await self.accept()
        print(f"Connected to agent with IP: {self.agent_ip}")
        await self.send(text_data=json.dumps({
            'type': 'auth',
            'message': 'Authentication required'
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from client: {data}")
        if 'type' not in data:
            return
        if data['type'] == 'auth':
            print("Authenticating agent")
            agent_info = data['info'] 
            await self.update_agent_in_db(
                ip=self.agent_ip,
                hostname=agent_info['hostname'],
                os=agent_info['os'],
                mac=agent_info['mac_address'],
                version=agent_info['version_number'],
            )
            await self.send(text_data=json.dumps({
                'type': 'auth',
                'message': 'Authentication successful'
            }))
        if data['type'] == 'event':
            event_data = data['info']
            await self.push_event(event_data)
            await self.send(text_data=json.dumps({
                'type': 'event',
                'message': 'Event received'
            }))
    
    async def disconnect(self, close_code):
        print(f"Closed with code: {close_code}")
        await self.agent_disconnect()
        await self.close()

    async def send_data(self, data):
        await self.send(text_data=json.dumps(data))

    async def reverse_shell(self, data):
        # This method will handle the "reverse_shell" type messages
        message = data['message']
        await self.send(text_data=json.dumps({
            'type': 'reverse_shell',
            'message': message
        }))

    @database_sync_to_async
    def update_agent_in_db(self, **kwargs):
        AgentItem.update_agent_in_db(**kwargs)

    @database_sync_to_async
    def push_event(self, event_data):
        EventManager.push_event(event_data)

    @database_sync_to_async
    def agent_disconnect(self):
        agent = AgentItem.objects.get(ip=self.agent_ip)
        agent.disconnect()