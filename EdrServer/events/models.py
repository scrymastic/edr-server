
from django.db import models
from uuid import uuid4


class Event(models.Model):
    universal_id = models.CharField(max_length=200, primary_key=True, default=uuid4)
    provider = models.JSONField(blank=True, default=dict)
    event_id = models.IntegerField()
    version = models.IntegerField()
    level = models.IntegerField()
    task = models.IntegerField()
    opcode = models.IntegerField()
    keywords = models.CharField(max_length=200)
    time_created = models.JSONField(blank=True, default=dict)
    event_record_id = models.IntegerField()
    correlation = models.JSONField(blank=True, default=dict)
    execution = models.JSONField(blank=True, default=dict)
    channel = models.CharField(max_length=200)
    computer = models.CharField(max_length=200)
    security = models.JSONField(blank=True, default=dict)

    event_data = models.JSONField(blank=True, default=dict)
