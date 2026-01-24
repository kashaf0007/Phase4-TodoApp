"""
Security utilities for the application
"""
import hashlib
import secrets
from typing import List
from ..config import DOMAIN_ALLOWLIST

def hash_password(password: str) -> str:
    """
    Hash a password using a salt
    """
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    salt = hashed_password[:32]
    stored_pwdhash = hashed_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_pwdhash

def is_valid_domain(domain: str) -> bool:
    """
    Check if the domain is in the allowlist
    """
    return domain in DOMAIN_ALLOWLIST

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Basic sanitization - in a real implementation, you'd want more comprehensive sanitization
    return input_str.strip()