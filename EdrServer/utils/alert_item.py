
from __future__ import annotations
from django.conf import settings
from django.db.models.query import QuerySet
from alerts.models import Alert
from utils.event_item import EventItem
from utils.rule_item import RuleItem
from pytz import timezone as pytz_timezone
from collections import Counter


class AlertItem(Alert):

    @staticmethod
    def from_dict(alert_dict) -> AlertItem:
        alert = AlertItem(
            event = EventItem.objects.get(universal_id=alert_dict['event_universal_id']),
            rule = RuleItem.objects.get(id=alert_dict['rule_id']),
            time_filtered=alert_dict['time_filtered']
        )
        return alert
    

    @staticmethod
    def search_alerts(query: str) -> QuerySet[AlertItem]:
        # return [AlertItem.from_dict(alert) for alert in AlertItem.objects.filter(query)]
        pass

    @staticmethod
    def get_level_distribution() -> dict:
        alert_levels = AlertItem.objects.values_list('rule__level', flat=True)
        level_counts = Counter(alert_levels)
        custom_order = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
        sorted_level_counts = dict(sorted(level_counts.items(), key=lambda item: (custom_order.get(item[0], float('inf')), item[0])))

        return sorted_level_counts
    
    @staticmethod
    def format_filtered_time(filtered_time) -> str:
        local_tz = pytz_timezone(settings.TIME_ZONE)
        dt_local = filtered_time.astimezone(local_tz)
        formatted_str = dt_local.strftime("%d/%m/%Y %H:%M:%S:%f")[:-3]
        return formatted_str
