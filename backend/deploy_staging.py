"""
Deployment script for staging environment
"""
import os
import subprocess
import sys
from pathlib import Path

def deploy_to_staging():
    """
    Deploy the application to staging environment
    """
    print("Starting deployment to staging environment...")
    
    # Check if we're in the correct directory
    if not Path("backend").exists():
        print("Error: backend directory not found. Make sure you're running this from the project root.")
        sys.exit(1)
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
    
    # Run tests to ensure everything works
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "backend/tests/", "-v"], check=False)
    if result.returncode != 0:
        print("Tests failed. Aborting deployment.")
        sys.exit(1)
    
    # Set staging environment variables
    os.environ["ENVIRONMENT"] = "staging"
    os.environ["DEBUG"] = "False"
    
    # Check if environment variables are properly set
    required_vars = ["NEON_DATABASE_URL", "BETTER_AUTH_SECRET", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {missing_vars}")
        print("Please set these variables before running the application.")
    
    print("Deployment to staging completed successfully!")
    print("\nTo start the application, run:")
    print("cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000")

def validate_deployment():
    """
    Validate the deployment by checking key components
    """
    print("Validating deployment...")
    
    # Check if required files exist
    required_files = [
        "backend/app/main.py",
        "backend/app/models/task.py",
        "backend/app/services/task_service.py",
        "backend/mcp/server.py",
        "backend/mcp/tools/add_task.py",
        "backend/requirements.txt",
        "backend/pyproject.toml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: Missing required files: {missing_files}")
        return False
    
    print("All required files are present.")
    
    # Check if dependencies are installed
    try:
        import fastapi
        import sqlmodel
        import pytest
        print("Dependencies are properly installed.")
    except ImportError as e:
        print(f"Error: Missing dependency: {e}")
        return False
    
    return True

if __name__ == "__main__":
    deploy_to_staging()
    if validate_deployment():
        print("\n✓ Deployment validation passed!")
    else:
        print("\n✗ Deployment validation failed!")
        sys.exit(1)