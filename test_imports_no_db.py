"""
Test script to verify imports are working correctly without database connection
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports_without_db():
    print("Testing imports without database connection...")
    
    try:
        # Test importing the main modules without triggering database connection
        import backend.src.main
        print("[OK] Successfully imported backend.src.main module")
        
        # Test importing the chat service
        import backend.services.chat_service
        print("[OK] Successfully imported backend.services.chat_service module")
        
        # Test importing models
        import backend.src.models.conversation
        import backend.src.models.message
        print("[OK] Successfully imported backend.src.models modules")
        
        # Test importing routes
        import backend.src.api.routes.chat
        print("[OK] Successfully imported backend.src.api.routes.chat module")
        
        print("\nAll imports successful! The module resolution issue has been fixed.")
        print("Note: Actual application startup requires database configuration.")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports_without_db()