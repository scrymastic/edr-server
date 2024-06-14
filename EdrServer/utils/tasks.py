
from __future__ import absolute_import, unicode_literals
from urllib.parse import urlparse
from typing import Dict, List
from celery import shared_task, Celery
from celery.schedules import crontab
from django.conf import settings
from django.utils import timezone
from EdrServer.celery import app
from utils.filter_engine import FilterEngine
from utils.event_item import EventItem
from utils.alert_item import AlertItem
from utils.errors import *
import redis
import json

# Connect to Redis
url = urlparse(settings.CELERY_BROKER_URL)
pool = redis.ConnectionPool(host=url.hostname, port=url.port)
redis_conn = redis.Redis(connection_pool=pool)


@shared_task
def process_event_redis(event: Dict) -> ERROR_CODE:
    try:
        for rule_id, rule in redis_conn.hgetall("rules").items():
            rule_id = rule_id.decode()
            rule = json.loads(rule)
            if FilterEngine.match_rule(rule, event):
                alert = {
                    "event_universal_id": EventItem.get_field(event, 'UniversalID'),
                    "rule_id": rule_id,
                    "time_filtered": timezone.now().isoformat()
                }
                redis_conn.rpush("alerts", json.dumps(alert))
        return ERROR_SUCCESS
    except Exception as e:
        return ERROR_FAILED
    

@shared_task
def save_event_db(event: Dict) -> ERROR_CODE:
    try:
        EventItem.from_dict(event).save()
        return ERROR_SUCCESS
    except Exception as e:
        return ERROR_FAILED
    

@shared_task
def deploy_rule_redis(rule_id: str, rule: Dict) -> ERROR_CODE:
    try:
        redis_conn.hset("rules", rule_id, json.dumps(rule))
        return ERROR_SUCCESS
    except Exception as e:
        return ERROR_FAILED
    

def undeploy_rule_redis(rule_id: str) -> ERROR_CODE:
    try:
        redis_conn.hdel("rules", rule_id)
        return ERROR_SUCCESS
    except Exception as e:
        return ERROR_FAILED


def get_alerts_redis() -> List[Dict]:
    alerts = []
    while True:
        alert = redis_conn.rpop("alerts")
        if not alert:
            break
        alerts.append(json.loads(alert))
    return alerts


@shared_task
def db_cleanup() -> ERROR_CODE:
    try:
        # Keep first 10000 events
        events = EventItem.objects.all().order_by("time_created")
        if len(events) > 10000:
            events[10000:].delete()
        return ERROR_SUCCESS
    except Exception as e:
        return ERROR_FAILED


app.conf.beat_schedule = {
    'db-cleanup': {
        'task': 'utils.tasks.db_cleanup',
        'schedule': crontab(minute=0, hour=0)
    }
}
