
from django.core.checks import register, Tags
from utils.rule_engine import RuleEngine
import time

@register(Tags.compatibility)
def init_rules(app_configs, **kwargs):
    print("Init rules...")
    start = time.time()
    RuleEngine.init_rules()
    print("Rules initialized.")
    print(f"Time taken: {time.time() - start} seconds")
    return []