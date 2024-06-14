
from typing import Dict


ERROR_FAILED = 0
ERROR_SUCCESS = 1
ERROR_INVALID_RULE = 2
ERROR_RULE_IS_ACTIVE = 3
ERROR_RULE_ALREADY_EXISTS = 4
ERROR_RULE_DOES_NOT_EXIST = 5
ERROR_RULE_ID_MISMATCH = 6
ERROR_REDIS_CONNECTION = 7
ERROR_DATABASE_CONNECTION = 8

ERROR_CODE = int

def error_to_info(error_code: int) -> str:
    if error_code == ERROR_SUCCESS:
        return "Success"
    elif error_code == ERROR_INVALID_RULE:
        return "Invalid rule"
    elif error_code == ERROR_RULE_IS_ACTIVE:
        return "Rule is active"
    elif error_code == ERROR_RULE_ALREADY_EXISTS:
        return "Rule already exists"
    elif error_code == ERROR_RULE_DOES_NOT_EXIST:
        return "Rule does not exist"
    elif error_code == ERROR_RULE_ID_MISMATCH:
        return "Rule ID mismatch"
    elif error_code == ERROR_REDIS_CONNECTION:
        return "Redis connection error"
    elif error_code == ERROR_DATABASE_CONNECTION:
        return "Database connection error"
    else:
        return "Failed"
    

def error_to_json(error_code: int) -> Dict:
    if error_code == ERROR_SUCCESS:
        return {"status": "success", "info": error_to_info(error_code)}
    else:
        return {"status": "error", "info": error_to_info(error_code)}