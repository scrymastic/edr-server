from django.db import models


class Agent(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    hostname = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)
    last_seen = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=True)

