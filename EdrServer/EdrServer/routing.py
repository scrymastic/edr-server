
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from EdrServer.consumers import EchoConsumer, AgentConsumer

websocket_urlpatterns = [
    path('ws/echo/', EchoConsumer.as_asgi()),
    path('ws/agent/', AgentConsumer.as_asgi()),
]