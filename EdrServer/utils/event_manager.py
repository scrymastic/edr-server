
from utils.singleton import Singleton
from utils.tasks import process_event_redis, save_event_db
from utils.event_item import EventItem
from typing import Dict, List

from utils.errors import *


class EventManager(metaclass=Singleton):

    def push_events(self, events: List[Dict]) -> ERROR_CODE:
        for event in events:
            self.push_event(event)
        return ERROR_SUCCESS
    

    def push_event(self, event: Dict) -> ERROR_CODE:
        process_event_redis.delay(event)
        save_event_db.delay(event)
        return ERROR_SUCCESS
    

    def get_event(self, universal_id: str) -> Dict:
        return EventItem.objects.get(universal_id=universal_id).to_dict()
