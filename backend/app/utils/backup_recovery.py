"""
Backup and recovery procedures
"""
import os
import shutil
import zipfile
import tempfile
from datetime import datetime
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class BackupManager:
    """
    Manages database backups and recovery procedures
    """
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, db_path: str, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of the database
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.zip"
        
        backup_path = self.backup_dir / backup_name
        
        try:
            # Create a temporary copy of the database file
            with tempfile.NamedTemporaryFile(delete=False) as temp_db:
                shutil.copy2(db_path, temp_db.name)
                
                # Create a zip archive containing the database
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(temp_db.name, os.path.basename(db_path))
                
                # Clean up the temporary file
                os.unlink(temp_db.name)
            
            logger.info(f"Backup created successfully: {backup_path}")
            return str(backup_path)
        
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    def list_backups(self) -> list:
        """
        List all available backups
        """
        backups = []
        for file in self.backup_dir.glob("*.zip"):
            stat = file.stat()
            backups.append({
                "name": file.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created"], reverse=True)
        return backups
    
    def restore_from_backup(self, backup_name: str, db_path: str) -> bool:
        """
        Restore database from a backup
        """
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            logger.error(f"Backup file does not exist: {backup_path}")
            return False
        
        try:
            # Extract the database file from the backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Get the database file name inside the zip
                db_filename = os.path.basename(db_path)
                
                # Extract to a temporary location first
                with tempfile.TemporaryDirectory() as temp_dir:
                    extracted_path = zipf.extract(db_filename, path=temp_dir)
                    
                    # Move the extracted file to the target location
                    target_path = Path(db_path)
                    if target_path.exists():
                        # Create a backup of the current database before overwriting
                        backup_current = f"{db_path}.restore_backup"
                        shutil.copy2(db_path, backup_current)
                        logger.info(f"Current database backed up to: {backup_current}")
                    
                    shutil.move(extracted_path, db_path)
            
            logger.info(f"Database restored successfully from: {backup_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to restore from backup: {str(e)}")
            return False

# Global backup manager instance
backup_manager = BackupManager()

def get_backup_manager() -> BackupManager:
    """Get the global backup manager instance"""
    return backup_manager