
from django.shortcuts import render
from utils.rule_item import RuleItem
from utils.event_item import EventItem
from utils.alert_item import AlertItem
import json


def view_dashboard(request):
    alert_level_distribution = AlertItem.get_level_distribution()
    event_event_id_distribution = EventItem.get_event_id_distribution()

    alert_labels = list(alert_level_distribution.keys())
    alert_data = list(alert_level_distribution.values())
    alert_data = {
        'labels': alert_labels,
        'datasets': [{
            'data': alert_data,
            'backgroundColor': ['#4CAF50', '#FFC107', '#F44336', '#B71C1C']  # Using a darker red for Critical
        }]
    }

    events_labels = [RuleItem.get_expected_category(event_id) for event_id in event_event_id_distribution.keys()]
    events_data = list(event_event_id_distribution.values())
    print(events_labels)
    print(events_data)
    events_data = {
        'labels': events_labels,
        'datasets': [{
            'label': 'Event Count',
            'data': events_data,
            'backgroundColor': 'rgba(54, 162, 235, 0.8)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }

    context = {
        'alert_chart_data': json.dumps(alert_data),
        'events_chart_data': json.dumps(events_data),
    }
    return render(request, 'dashboard/dashboard.html', context)