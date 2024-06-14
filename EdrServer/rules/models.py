
from django.db import models


class Rule(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    id = models.CharField(max_length=200, primary_key=True)
    related = models.JSONField(blank=True, default=list)
    status = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    references = models.JSONField(blank=True, default=list)
    author = models.CharField(max_length=200, blank=True, default="")
    tags = models.JSONField(blank=True, default=list)
    logsource = models.JSONField(blank=True, default=dict)
    detection = models.JSONField(blank=True, default=dict)
    tags = models.JSONField(blank=True, default=list)
    logsource = models.JSONField(blank=True, default=dict)
    detection = models.JSONField(blank=True, default=dict)
    falsepositives = models.JSONField(blank=True, default=list)
    level = models.CharField(max_length=200, blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=False)
    

