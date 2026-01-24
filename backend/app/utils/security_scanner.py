"""
Security scanning utilities
"""
import re
import logging
from typing import Dict, List, Any
from .exceptions import InvalidParametersException

logger = logging.getLogger(__name__)

class SecurityScanner:
    """
    Performs security checks on inputs and data
    """
    
    # Common patterns for potential security issues
    SECURITY_PATTERNS = {
        'sql_injection': [
            r"(?i)(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
            r"(?i)(\b(OR|AND)\s+[\d=']+\s*[=<>]\s*[\d=']+)",
            r"(?i)(\b(OR|AND)\s+[\d=']+\s*[=<>]\s*[\d=']+)",
            r"(?i)(\b(OR|AND)\s+[\d=']+\s*[=<>]\s*[\d=']+)",
            r"(?i)(\b(OR|AND)\s+[\d=']+\s*[=<>]\s*[\d=']+)"
        ],
        'xss_script': [
            r"(?i)<script[^>]*>.*?</script>",
            r"(?i)<iframe[^>]*>.*?</iframe>",
            r"(?i)<object[^>]*>.*?</object>",
            r"(?i)<embed[^>]*>.*?</embed>",
            r"(?i)<link[^>]*>",
            r"(?i)<meta[^>]*>"
        ],
        'path_traversal': [
            r"\.\./",  # Unix-style
            r"\.\.\\",  # Windows-style
            r"%2e%2e%2f",  # URL-encoded
            r"\.\.\%2f"   # Mixed encoding
        ]
    }
    
    def scan_input(self, input_str: str) -> Dict[str, List[str]]:
        """
        Scan an input string for potential security issues
        """
        issues = {}
        
        for category, patterns in self.SECURITY_PATTERNS.items():
            found_issues = []
            for pattern in patterns:
                matches = re.findall(pattern, input_str)
                if matches:
                    found_issues.extend(matches)
            
            if found_issues:
                issues[category] = found_issues
        
        return issues
    
    def validate_input(self, input_str: str, context: str = "general") -> bool:
        """
        Validate an input string for security issues
        """
        issues = self.scan_input(input_str)
        
        if issues:
            logger.warning(f"Security issues found in {context}: {issues}")
            return False
        
        return True
    
    def sanitize_sql_query(self, query: str) -> str:
        """
        Basic sanitization for SQL queries (not a complete solution)
        """
        # This is a very basic sanitization - in practice, use parameterized queries
        sanitized = re.sub(r"[;'\"]", "", query)
        return sanitized
    
    def validate_json_payload(self, payload: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate a JSON payload for security issues
        """
        issues = {}
        
        def scan_recursive(obj, path=""):
            if isinstance(obj, str):
                obj_issues = self.scan_input(obj)
                if obj_issues:
                    issues[path or "root"] = obj_issues
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    scan_recursive(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    scan_recursive(item, new_path)
        
        scan_recursive(payload)
        return issues

# Global security scanner instance
security_scanner = SecurityScanner()

def get_security_scanner() -> SecurityScanner:
    """Get the global security scanner instance"""
    return security_scanner

def validate_secure_input(input_str: str, context: str = "general") -> bool:
    """
    Convenience function to validate input security
    """
    return security_scanner.validate_input(input_str, context)

def scan_for_security_issues(input_str: str) -> Dict[str, List[str]]:
    """
    Convenience function to scan for security issues
    """
    return security_scanner.scan_input(input_str)