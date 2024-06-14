
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import UploadFileForm
from utils.event_item import EventItem
from utils.log_parser import LogParser
from utils.event_manager import EventManager

from utils.errors import error_to_json, ERROR_FAILED, ERROR_SUCCESS


def view_events(request):
    # EventItem.objects.all().delete()
    events = EventItem.objects.all().order_by('-time_created')
    event_table = []
    for event in events:
        event_item = {
            'time_created_system_time': EventItem.format_system_time(
                event.time_created_system_time),
            'computer': event.computer,
            'channel': event.channel,
            'event_id': event.event_id,
            'universal_id': event.universal_id,
        }
        event_table.append(event_item)

    events_per_page = 200
    paginator = Paginator(event_table, events_per_page)
    page_number = request.GET.get('page', 1)
    events = paginator.get_page(page_number)
    return render(request, 'events/view_events.html', {'item_page': events})


def read_events(request):
    form = UploadFileForm()
    events = request.session.get('event_table', [])
    event_table = []
    for event in events:
        event_item = {
            'time_created_system_time': EventItem.format_system_time(
                EventItem.get_field(event, 'System', 'TimeCreated', 'SystemTime')),
            'computer': EventItem.get_field(event, 'System', 'Computer'),
            'channel': EventItem.get_field(event, 'System', 'Channel'),
            'event_id': EventItem.get_field(event, 'System', 'EventID'),
            'universal_id': EventItem.get_field(event, 'UniversalID'),
        }
        event_table.append(event_item)
    events_per_page = 200
    paginator = Paginator(event_table, events_per_page)
    page_number = request.GET.get('page', 1)
    events = paginator.get_page(page_number)
    return render(request, 'events/read_events.html', {'form': form, 'item_page': events})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = form.save_file()
            log_parser = LogParser()
            events = log_parser.parse_log_file(file_path)
            event_table = [EventItem.assign_event_universal_id(event) for event in events]
            request.session['event_table'] = event_table
            return redirect('read_events')
    else:
        form = UploadFileForm()
    return render(request, 'events/read_events.html',
                  {'form': form})


def get_event(request):
    universal_id = request.GET.get('universal_id')
    event_table = request.session.get('event_table', [])
    event = [event for event in event_table if EventItem.get_field(event, 'UniversalID') == universal_id]
    if event:
        event = event[0]
        return JsonResponse(event)
    event = EventItem.objects.get(universal_id=universal_id).to_dict()
    return JsonResponse(event)


def push_events(request):
    universal_ids = request.GET.getlist('universal_ids[]')
    event_manager = EventManager()
    event_table = request.session.get('event_table', [])
    events = [event for event in event_table if EventItem.get_field(event, 'UniversalID') in universal_ids]
    error_code = event_manager.push_events(events)
    response = error_to_json(error_code)
    if error_code == ERROR_SUCCESS:
        response['message'] = f'{len(events)} events pushed successfully'
    else:
        response['message'] = 'Failed to push events'
    return JsonResponse(response)


