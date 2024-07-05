
from utils.singleton import Singleton
from utils.tasks import process_event_redis
from utils.event_item import EventItem
from typing import Dict, List

from utils.errors import *


class EventManager(metaclass=Singleton):

    def push_events(self, events: List[Dict]) -> ERROR_CODE:
        for event in events:
            EventManager.push_event(event)
        return ERROR_SUCCESS
    
    @staticmethod
    def push_event(event: Dict) -> ERROR_CODE:
        process_event_redis.delay(event)
        return ERROR_SUCCESS
    
    @staticmethod
    def get_event(universal_id: str) -> Dict:
        return EventItem.objects.get(universal_id=universal_id).to_dict()
