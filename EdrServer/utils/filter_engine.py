

from utils.rule_item import RuleItem
from utils.event_item import EventItem
from utils.singleton import Singleton
from typing import Union, Dict, List, Any
from base64 import b64decode
from ipaddress import ip_network
import re



def all_of(*args):
    return all(args) 
def any_of(*args):
    return any(args)


class FilterEngine(metaclass=Singleton):
    """
    A class that implements a filter engine for filtering events based on rules defined in Sigma format.
    """

    @staticmethod
    def match_block(block: Union[Dict, List], event: Dict) -> bool:
        """
        Match a block of expressions against an event.
        E.g.: selection, filter, etc.
        """
        if isinstance(block, dict):
            return all(FilterEngine.match_expression(expression, value, event)
                       for expression, value in block.items())
        elif isinstance(block, list):
            return any(FilterEngine.match_expression(expression, value, event)
                       for condition in block for expression, value in condition.items())
            # condition might be a string in some cases, not handled here
        else:
            raise ValueError('Unexpected value type:', block)
    

    @staticmethod
    def match_expression(expression: str, value: Any, event: Dict) -> bool:
        if '|' in expression:
            field, operator = expression.split('|', 1)
        else:
            field = expression
            operator = None

        if field == 'EventID':
            event_field = EventItem.get_field(event, 'System', 'EventID')
        else:
            event_field = EventItem.get_field(event, 'EventData', field)

        if event_field is None:
            return False
        
        if not isinstance(value, list):
            value = [value]
        
        match operator:
            case None:
                return all(event_field == val for val in value) # value has only one element
            case 'startswith':
                return any(event_field.startswith(val) for val in value)
            case 'endswith':
                return any(event_field.endswith(val) for val in value)
            case 'contains':
                return any(val in event_field for val in value)
            case 'contains|windash':
                return any(val in event_field for val in value)
            case 'contains|all':
                return all(val in event_field for val in value)
            case 'contains|all|windash':
                return all(val in event_field for val in value)
            case 'base64offset|contains':
                try:
                    event_field = b64decode(event_field).decode('utf-8')
                except ValueError as e:
                    return False
                return any(val in event_field for val in value)
            case 're':
                return any(re.match(val, event_field) for val in value)
            case 'cidr':
                return any(ip_network(val).overlaps(ip_network(event_field)) for val in value)
            
            case 'not startswith':
                return all(not event_field.startswith(val) for val in value)
            case 'not endswith':
                return all(not event_field.endswith(val) for val in value)
            case 'not contains':
                return all(val not in event_field for val in value)
            case 'not contains|all':
                return not all(val in event_field for val in value)
            case 'not re':
                return all(not re.match(val, event_field) for val in value)
            case 'not cidr':
                return all(not ip_network(val).overlaps(ip_network(event_field)) for val in value)
            
            case _:
                raise ValueError(f'Unsupported operator in expression: {expression}')
            
    
    @staticmethod
    def match_logsource(logsource: Dict, event: Dict) -> bool:
        event_id = EventItem.get_field(event, 'System', 'EventID')
        if not isinstance(event_id, int):
            # logging.error(f"EventID is not an integer: {event_id}")
            return False
        if expected_category := RuleItem.get_expected_category(event_id):
            return expected_category == logsource.get('category', None)
        return True


    @staticmethod
    def match_rule(rule: Dict, event: Dict) -> bool:
        try:
            eval_expr = RuleItem.get_field(rule, 'detection', 'evaluation')
            return eval(eval_expr)
        except Exception as e:
            return False



if __name__ == '__main__':
    pass