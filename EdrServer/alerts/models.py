
from django.db import models
from utils.event_item import EventItem
from utils.rule_item import RuleItem


class Alert(models.Model):
    event = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    rule = models.ForeignKey(RuleItem, on_delete=models.CASCADE)
    time_filtered = models.DateTimeField(auto_now_add=True)

