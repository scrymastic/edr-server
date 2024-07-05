

from django.urls import path
from . import views


urlpatterns = [
    path('agents/', views.view_agents, name='agents'),
    path('agents/get_agent_sysinfo/', views.get_agent_sysinfo, name='get_agent_sysinfo'),
    path('agents/send_connection_request', views.send_connection_request, name='send_connection_request'),
]

