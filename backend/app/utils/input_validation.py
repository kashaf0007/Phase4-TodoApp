"""
Input validation and sanitization utilities
"""
import html
import re
from typing import Any, Dict, List
from .exceptions import InvalidParametersException

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    if not input_str:
        return input_str
    
    # Remove HTML tags
    sanitized = html.escape(input_str)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';]', '', sanitized)
    
    return sanitized.strip()

def validate_and_sanitize_inputs(data: Dict[str, Any], validation_rules: Dict[str, dict]) -> Dict[str, Any]:
    """
    Validate and sanitize input data based on provided rules
    """
    errors = {}
    sanitized_data = {}
    
    for field, value in data.items():
        if field in validation_rules:
            rules = validation_rules[field]
            
            # Apply sanitization
            if isinstance(value, str):
                sanitized_value = sanitize_input(value)
            else:
                sanitized_value = value
            
            # Apply validation rules
            if rules.get("required") and value is None:
                errors[field] = f"{field} is required"
                continue
            
            if value is not None:
                if "min_length" in rules and len(str(value)) < rules["min_length"]:
                    errors[field] = f"{field} must be at least {rules['min_length']} characters"
                
                if "max_length" in rules and len(str(value)) > rules["max_length"]:
                    errors[field] = f"{field} must be no more than {rules['max_length']} characters"
                
                if "regex" in rules and not re.match(rules["regex"], str(value)):
                    errors[field] = f"{field} does not match required format"
            
            sanitized_data[field] = sanitized_value
        else:
            # For fields without specific rules, still sanitize if it's a string
            if isinstance(value, str):
                sanitized_data[field] = sanitize_input(value)
            else:
                sanitized_data[field] = value
    
    if errors:
        raise InvalidParametersException(errors)
    
    return sanitized_data

def validate_list_input(items: List[Any], max_items: int = 100) -> List[Any]:
    """
    Validate list inputs to prevent abuse
    """
    if len(items) > max_items:
        raise InvalidParametersException({f"list": f"Too many items, maximum allowed is {max_items}"})
    
    return items