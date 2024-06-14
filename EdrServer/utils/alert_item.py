
from __future__ import annotations
from alerts.models import Alert
from utils.event_item import EventItem
from utils.rule_item import RuleItem


class AlertItem(Alert):

    @staticmethod
    def from_dict(alert_dict) -> AlertItem:
        alert = AlertItem(
            event = EventItem.objects.get(universal_id=alert_dict['event_universal_id']),
            rule = RuleItem.objects.get(id=alert_dict['rule_id']),
            time_filtered=alert_dict['time_filtered']
        )
        return alert