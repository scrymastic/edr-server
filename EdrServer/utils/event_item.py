
from __future__ import annotations
from django.db.models import Q
from django.db.models.query import QuerySet
from django.conf import settings
from events.models import Event
from typing import Any, Dict, List
from uuid import uuid4
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from django.db.models import Count
import yaml
import re


class EventItem(Event):

    def to_dict(self) -> Dict:
        return {
            "UniversalID": self.universal_id,
            "System": {
                "Provider": self.provider,
                "EventID": self.event_id,
                "Version": self.version,
                "Level": self.level,
                "Task": self.task,
                "Opcode": self.opcode,
                "Keywords": self.keywords,
                "TimeCreated": self.time_created,
                "EventRecordID": self.event_record_id,
                "Correlation": self.correlation,
                "Execution": self.execution,
                "Channel": self.channel,
                "Computer": self.computer,
                "Security": self.security
            },
            "EventData": self.event_data
        }
    

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict())
    

    @staticmethod
    def assign_event_universal_id(event: Dict) -> Dict:
        event["UniversalID"] = str(uuid4())
        return event
    

    @staticmethod
    def is_valid_event(event: Dict) -> bool:
        if not isinstance(event, dict):
            return False
        # check for required fields
        universal_id = event.get("UniversalID")
        if not universal_id or not isinstance(universal_id, str):
            return False
        system = event.get("System")
        if not system or not isinstance(system, dict):
            return False
        provider = system.get("Provider")
        if not provider or not isinstance(provider, dict):
            return False
        event_id = system.get("EventID")
        if not event_id or not isinstance(event_id, int):
            return False
        version = system.get("Version")
        if not version or not isinstance(version, int):
            return False
        level = system.get("Level")
        if not level or not isinstance(level, int):
            return False
        task = system.get("Task")
        if not task or not isinstance(task, int):
            return False
        opcode = system.get("Opcode")
        if not opcode or not isinstance(opcode, int):
            return False
        keywords = system.get("Keywords")
        if not keywords or not isinstance(keywords, str):
            return False
        time_created = system.get("TimeCreated")
        if not time_created or not isinstance(time_created, dict):
            return False
        event_record_id = system.get("EventRecordID")
        if not event_record_id or not isinstance(event_record_id, int):
            return False
        correlation = system.get("Correlation")
        if correlation and not isinstance(correlation, dict):
            return False
        execution = system.get("Execution")
        if not execution or not isinstance(execution, dict):
            return False
        channel = system.get("Channel")
        if not channel or not isinstance(channel, str):
            return False
        computer = system.get("Computer")
        if not computer or not isinstance(computer, str):
            return False
        security = system.get("Security")
        if not security or not isinstance(security, dict):
            return False
        event_data = event.get("EventData")
        if not event_data or not isinstance(event_data, dict):
            return False
        return True
    

    @staticmethod
    def from_dict(event_dict: Dict) -> EventItem:
        system = event_dict.get("System", {})
        return EventItem(
            universal_id = event_dict.get("UniversalID"),
            provider = system.get("Provider"),
            event_id = system.get("EventID"),
            version = system.get("Version"),
            level = system.get("Level"),
            task = system.get("Task"),
            opcode = system.get("Opcode"),
            keywords = system.get("Keywords"),
            time_created = system.get("TimeCreated"),
            event_record_id = system.get("EventRecordID"),
            correlation = system.get("Correlation"),
            execution = system.get("Execution"),
            channel = system.get("Channel"),
            computer = system.get("Computer"),
            security = system.get("Security", {}),
            event_data = event_dict.get("EventData")
        )
    

    @staticmethod
    def get_field(event: Dict, *keys) -> Any:
        for key in keys:
            if not isinstance(event, dict):
                return None
            event = event.get(key)
        return event
    

    @staticmethod
    def convert_utc_to_local(system_time: str) -> str:
        system_time = system_time[:23] + 'Z'
        dt_utc = datetime.strptime(system_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        
        local_tz = pytz_timezone(settings.TIME_ZONE)
        dt_local = dt_utc.astimezone(local_tz)
        formatted_str = dt_local.strftime("%d/%m/%Y %H:%M:%S:%f")[:-3]

        return formatted_str
    

    @staticmethod
    def search_events(search_str: str) -> QuerySet[EventItem]:
        '''
        Search for events based on the search string.
        Format: field1="value1" AND field2~"value2" OR ...
        '''
        print("Search string:", search_str)
        if not search_str:
            return EventItem.objects.all()

        single_query = r'([\w\d]+)\s*([~=<>])\s*"([^"]*)"'
        pattern = single_query + r'|\b(AND|OR)\b'
        def split_pattern_string(input_string, pattern):
            # The pattern to match individual conditions and logical operators
            matches = re.findall(pattern, input_string)
            result = []
            for match in matches:
                if match[3]:
                    result.append(match[3])
                else:
                    result.append(f'{match[0]}{match[1]}"{match[2]}"')
            return result
        
        query = []
        for token in split_pattern_string(search_str, pattern):
            if token == 'AND':
                query.append('&')
            elif token == 'OR':
                query.append('|')
            else:
                field, operator, value = re.match(single_query, token).groups()
                if operator == '=':
                    query.append('Q({}="{}")'.format(field, value))
                elif operator == '~':
                    query.append('Q({}__icontains="{}")'.format(field, value))
                elif operator == '>':
                    query.append('Q({}__gt="{}")'.format(field, value))
                elif operator == '<':
                    query.append('Q({}__lt="{}")'.format(field, value))
                else:
                    return None
        query_str = ' '.join(query)
        try:
            events = EventItem.objects.filter(eval(query_str))
        except Exception as e:
            print("Error in search_events:", e)
            print("Query:", query_str)
            events = None
        # print(events[0].time_created)
        return events
    

    @staticmethod
    def get_event_id_distribution() -> dict:
        event_counts = EventItem.objects.values('event_id').annotate(count=Count('event_id')).order_by()
        event_id_distribution = {item['event_id']: item['count'] 
                                 for item in event_counts if item['count'] > 0}
        return event_id_distribution


    @property
    def time_created_system_time(self) -> str:
        return self.time_created.get("SystemTime")

    
    @property
    def execution_process_id(self) -> int:
        return self.execution.get("ProcessID")
    
    @property
    def execution_thread_id(self) -> int:
        return self.execution.get("ThreadID")
    
    @property
    def provider_name(self) -> str:
        return self.provider.get("Name")
    
    @property
    def provider_guid(self) -> str:
        return self.provider.get("Guid")

    @property
    def provider_event_source_name(self) -> str:
        return self.provider.get("EventSourceName")
    
    @property
    def sercurity_user_id(self) -> str:
        return self.security.get("UserID")
    
