
from utils.tasks import get_alerts_redis
from utils.alert_item import AlertItem
from datetime import datetime


class AlertManager():

    @staticmethod
    def save_new_alerts():
        alerts = get_alerts_redis()
        for alert in alerts:
            alert['time_filtered'] = datetime.strptime(
                alert['time_filtered'], '%Y-%m-%dT%H:%M:%S.%f%z')
            AlertItem.from_dict(alert).save()
        return len(alerts)
    