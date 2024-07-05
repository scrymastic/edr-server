
from django.utils import timezone
from django.db import transaction
from utils.rule_item import RuleItem
from utils.singleton import Singleton
from utils.tasks import deploy_rule_redis, undeploy_rule_redis
from typing import Dict, List

from utils.errors import *



class RuleEngine(metaclass=Singleton):

    @staticmethod
    def add_rule(rule: Dict) -> ERROR_CODE:
        if not RuleItem.is_valid_rule(rule):
            return ERROR_INVALID_RULE
        rule_item = RuleItem.from_dict(rule)
        if not rule_item:
            return ERROR_INVALID_RULE
        if RuleItem.objects.filter(id=rule_item.id).exists():
            return ERROR_RULE_ALREADY_EXISTS
        rule = RuleItem(
            title=rule_item.title,
            id=rule_item.id,
            related=rule_item.related,
            status=rule_item.status,
            description=rule_item.description,
            references=rule_item.references,
            author=rule_item.author,
            tags=rule_item.tags,
            logsource=rule_item.logsource,
            detection=rule_item.detection,
            falsepositives=rule_item.falsepositives,
            level=rule_item.level,
            date=timezone.now(),
            modified=timezone.now(),
            is_active=False
        )
        rule.save()
        return ERROR_SUCCESS
        
    
    @staticmethod
    def remove_rule(rule_id: str) -> ERROR_CODE:
        rule = RuleItem.objects.get(id=rule_id)
        # Check if rule is active
        if rule.is_active:
            return ERROR_RULE_IS_ACTIVE
        rule.delete()
        return ERROR_SUCCESS


    @staticmethod
    def update_rule(rule_id: str, rule: Dict) -> ERROR_CODE:
        if not RuleItem.is_valid_rule(rule):
            return ERROR_INVALID_RULE
        rule_item = RuleItem.from_dict(rule)
        if not rule_item:
            return ERROR_INVALID_RULE
        rule = RuleItem.objects.get(id=rule_id)
        if rule.id != rule_item.id:
            return ERROR_RULE_ID_MISMATCH
        if rule.is_active:
            return ERROR_RULE_IS_ACTIVE
        rule.title = rule_item.title
        rule.related = rule_item.related
        rule.status = rule_item.status
        rule.description = rule_item.description
        rule.references = rule_item.references
        rule.author = rule_item.author
        rule.tags = rule_item.tags
        rule.logsource = rule_item.logsource
        rule.detection = rule_item.detection
        rule.falsepositives = rule_item.falsepositives
        rule.level = rule_item.level
        rule.date = rule_item.date
        rule.modified = timezone.now()

        rule.save()
        return ERROR_SUCCESS


    @staticmethod
    def deploy_rule(rule_id: str) -> ERROR_CODE:
        try:
            with transaction.atomic():
                rule = RuleItem.objects.get(id=rule_id)
                rule.is_active = True
                rule.save()
                result = deploy_rule_redis(rule_id, rule.to_rule_filter())
                if result != ERROR_SUCCESS:
                    raise Exception('Failed to deploy rule to Redis')
        except Exception as e:
            return ERROR_DATABASE_CONNECTION
        return ERROR_SUCCESS

    @staticmethod
    def undeploy_rule(rule_id: str) -> ERROR_CODE:
        try:
            with transaction.atomic():
                rule = RuleItem.objects.get(id=rule_id)
                rule.is_active = False
                rule.save()
                result = undeploy_rule_redis(rule_id)
                if result != ERROR_SUCCESS:
                    raise Exception('Failed to undeploy rule from Redis')
        except Exception as e:
            return ERROR_DATABASE_CONNECTION
        return ERROR_SUCCESS
    

    @staticmethod
    def init_rules() -> int:
        from django.conf import settings
        import yaml
        dir_path = settings.BASE_DIR / 'utils' / 'rules'
        for file_path in dir_path.glob('*.yml'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    # Load the YAML data
                    data = yaml.safe_load(file)
                    data.update({"is_active": True})
                    rule_item = RuleItem.from_dict(data)
                    if not rule_item:
                        print(f"Error reading {file_path}: Invalid rule")
                        continue
                    # Overwrite the existing rule if it exists
                    rule_item.save()
                except yaml.YAMLError as error:
                    print(f"Error reading {file_path}: {error}")
                    continue
        rules = RuleItem.objects.all()
        for rule in rules:
            if rule.is_active:
                deploy_rule_redis(rule.id, rule.to_rule_filter())

        return len(rules)





