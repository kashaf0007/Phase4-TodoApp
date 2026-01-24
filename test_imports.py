"""
Test script to verify imports are working correctly
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    print("Testing imports...")

    try:
        # Test importing the main app
        from backend.src.main import app
        print("[OK] Successfully imported backend.src.main:app")

        # Test importing the chat service
        from backend.services.chat_service import ChatService
        print("[OK] Successfully imported backend.services.chat_service:ChatService")

        # Test importing models
        from backend.src.models.conversation import Conversation
        from backend.src.models.message import Message
        print("[OK] Successfully imported backend.src.models")

        # Test importing routes
        from backend.src.api.routes.chat import router as chat_router
        print("[OK] Successfully imported backend.src.api.routes.chat")

        print("\nAll imports successful! The module resolution issue has been fixed.")
        return True

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()