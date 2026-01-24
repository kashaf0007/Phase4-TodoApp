"""
Validation utilities for the application
"""
from typing import Any, Dict
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_id(user_id: str) -> bool:
    """Validate user ID format"""
    # Assuming user IDs are UUIDs
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return re.match(pattern, user_id) is not None

def validate_task_title(title: str) -> bool:
    """Validate task title"""
    if not title or len(title) < 1 or len(title) > 255:
        return False
    return True

def validate_task_description(description: str) -> bool:
    """Validate task description"""
    if description and len(description) > 10000:  # Arbitrary limit
        return False
    return True

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Dict[str, str]:
    """Validate that required fields are present in data"""
    errors = {}
    for field in required_fields:
        if field not in data or data[field] is None:
            errors[field] = f"{field} is required"
    return errors

def validate_field_length(field_value: str, min_len: int = 0, max_len: int = None) -> bool:
    """Validate field length"""
    if field_value is None:
        return False
    if len(field_value) < min_len:
        return False
    if max_len and len(field_value) > max_len:
        return False
    return True