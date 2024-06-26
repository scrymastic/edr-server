
from django.core.checks import register, Tags
from utils.rule_engine import RuleEngine

@register(Tags.compatibility)
def init_rules(app_configs, **kwargs):
    RuleEngine.init_rules()
    return []