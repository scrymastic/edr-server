
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.event_item import EventItem
from utils.event_manager import EventManager
import json

@csrf_exempt
def receive_events(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        event = json.loads(data)
        event = EventItem.assign_event_universal_id(event)
        EventManager().push_event(event)
        return JsonResponse({'status': 'success', 'message': 'Events received successfully'}, status=200)
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)