
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from utils.alert_manager import AlertManager
from utils.alert_item import AlertItem
from utils.rule_item import RuleItem
from utils.event_item import EventItem


def view_alerts(request):
    # AlertItem.objects.all().delete()
    AlertManager.save_new_alerts()
    alerts = AlertItem.objects.all().order_by('-time_filtered')\
        .select_related('event', 'rule')
    print(alerts[0].time_filtered)
    alert_list = []
    for alert in alerts:
        event: EventItem = alert.event
        rule: RuleItem = alert.rule
        alert_item = {
            'time_filtered': AlertItem.format_filtered_time(
                alert.time_filtered),
            'title': rule.title,
            'level': rule.level,
            'computer': event.computer,
            'event_id': event.event_id,
            'event_universal_id': event.universal_id,
            'rule_id': rule.id,
        }
        alert_list.append(alert_item)
    alerts_per_page = 200
    paginator = Paginator(alert_list, alerts_per_page)
    page_number = request.GET.get('page', 1)
    alerts = paginator.get_page(page_number)
    return render(request, 'alerts/view_alerts.html', {'item_page': alerts})



def get_alert(request):
    rule_id = request.POST.get('rule_id')
    event_universal_id = request.POST.get('event_universal_id')
    rule = RuleItem.objects.get(id=rule_id)
    return JsonResponse({
        'rule': {
            'id': rule.id,
            'title': rule.title,
            'description': rule.description,
        },
        'event': EventItem.objects.get(universal_id=event_universal_id).to_dict()
    })


def search_alerts(request):
    pass

