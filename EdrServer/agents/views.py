
from django.shortcuts import render
from utils.agent_item import AgentItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

def view_agents(request):
    agents = AgentItem.objects.all().order_by('-last_seen')
    agent_list = [
        {
            'ip': agent.ip,
            'hostname': agent.hostname,
            'os': agent.os,
            'version': agent.version,
            'last_seen': agent.last_seen,
            'is_active': agent.is_active,
        }
        for agent in agents
    ]
    return render(request, 'agents/view_agents.html', {'items': agent_list})


def get_agent_sysinfo(request):
    pass



def send_connection_request(request):
    agent_ip = request.POST.get('agent_ip')
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            agent_ip,
            {
                "type": "reverse_shell",
                "message": "Requesting reverse shell connection"
            }
        )
        print(f"Message sent to agent with IP: {agent_ip}")
        return JsonResponse({"status": "success", "message": "Message sent"})
    except Exception as e:
        print(f"Failed to send message to agent with IP: {agent_ip}")
        print(f"Error: {str(e)}")
        return JsonResponse({"status": "failed", "message": "Failed to send message to agent"})