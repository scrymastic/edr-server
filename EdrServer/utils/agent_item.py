

from __future__ import annotations
from django.utils import timezone
from agents.models import Agent
from typing import Dict


class AgentItem(Agent):
    
    @staticmethod
    def from_dict(data: Dict) -> AgentItem:
        return AgentItem(
            ip=data["ip"],
            hostname=data["hostname"],
            os=data["os"],
            mac=data["mac"],
            version=data["version"],
            last_seen=data("last_seen", None),
            is_active=data.get("is_active", True)
        )

    @staticmethod
    def update_agent_in_db(ip=None, hostname=None, os=None, mac=None, version=None, last_seen=None, is_active=True) -> None:
        # Check if agent exists
        if not AgentItem.objects.filter(ip=ip).exists():
            AgentItem(
                ip=ip,
                hostname=hostname,
                os=os,
                mac=mac,
                version=version,
                last_seen=last_seen,
                is_active=is_active
            ).save()
            return

        agent = AgentItem.objects.get(ip=ip)
        if hostname:
            agent.hostname = hostname
        if os:
            agent.os = os
        if mac:
            agent.mac = mac
        if version:
            agent.version = version
        if last_seen:
            agent.last_seen = last_seen
        if is_active:
            agent.is_active = is_active
        agent.save()
    
    
    @staticmethod
    def agent_disconnect(ip: str) -> AgentItem:
        agent = AgentItem.objects.get(ip=ip)
        agent.last_seen = timezone.now()
        agent.is_active = False
        agent.save()
        return agent
    

    def disconnect(self) -> None:
        self.last_seen = timezone.now()
        self.is_active = False
        self.save()
