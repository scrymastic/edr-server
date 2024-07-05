
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
from utils.rule_item import RuleItem
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
            if not FilterEngine.match_rule(rule, event):
                event = EventItem.from_dict(event)
                event.save()
                return ERROR_SUCCESS
            try:
                event = EventItem.from_dict(event)
                rule = RuleItem.objects.get(id=rule_id)
                event.save()
                AlertItem(
                    event=event,
                    rule=rule,
                    time_filtered=timezone.now()
                ).save()
                return ERROR_SUCCESS
            except Exception as e:
                print('Error saving event to database:', e)
                return ERROR_FAILED
        return ERROR_SUCCESS
    except Exception as e:
        print('Error processing event:', e)
        return ERROR_FAILED
    


@shared_task
def deploy_rule_redis(rule_id: str, rule: Dict) -> ERROR_CODE:
    try:
        redis_conn.hset("rules", rule_id, json.dumps(rule))
        return ERROR_SUCCESS
    except Exception as e:
        print('Error deploying rule to Redis:', e)
        return ERROR_FAILED
    

def undeploy_rule_redis(rule_id: str) -> ERROR_CODE:
    try:
        redis_conn.hdel("rules", rule_id)
        return ERROR_SUCCESS
    except Exception as e:
        print('Error undeploying rule from Redis:', e)
        return ERROR_FAILED


# def get_alerts_redis() -> List[Dict]:
#     alerts = []
#     while True:
#         alert = redis_conn.rpop("alerts")
#         if not alert:
#             break
#         alerts.append(json.loads(alert))
#     return alerts


# def add_agent_redis(agent_ip: str, agent_info: Dict) -> ERROR_CODE:
#     try:
#         redis_conn.hset("agents", agent_ip, json.dumps(agent_info))
#         return ERROR_SUCCESS
#     except Exception as e:
#         return ERROR_FAILED
    

# def remove_agent_redis(agent_ip: str) -> ERROR_CODE:
#     try:
#         redis_conn.hdel("agents", agent_ip)
#         return ERROR_SUCCESS
#     except Exception as e:
#         return ERROR_FAILED


@shared_task
def db_cleanup() -> ERROR_CODE:
    try:
        # Keep first 10000 events
        events = EventItem.objects.all().order_by("time_created")
        if len(events) > 10000:
            events[10000:].delete()
        return ERROR_SUCCESS
    except Exception as e:
        print('Error cleaning up database:', e)
        return ERROR_FAILED


app.conf.beat_schedule = {
    'db-cleanup': {
        'task': 'utils.tasks.db_cleanup',
        'schedule': crontab(minute=0, hour=0)
    }
}
