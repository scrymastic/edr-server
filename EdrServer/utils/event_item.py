
from __future__ import annotations
from events.models import Event
from typing import Any, Dict
from uuid import uuid4
import yaml
from datetime import datetime, timezone


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
    def format_system_time(system_time: str) -> datetime:
        system_time = system_time[:23] + 'Z'
        dt = datetime.strptime(system_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return dt.replace(tzinfo=timezone.utc)


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
    
