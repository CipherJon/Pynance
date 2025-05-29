import os
import shutil
import logging
from datetime import datetime
import sqlite3
import json

logger = logging.getLogger(__name__)

def backup_database():
    """Create a backup of the database."""
    try:
        # Create backup directory if it doesn't exist
        backup_dir = os.path.join('data', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'database_backup_{timestamp}.db')
        
        # Copy database file
        shutil.copy2(os.path.join('data', 'database.db'), backup_file)
        
        # Export data as JSON for additional safety
        json_backup = os.path.join(backup_dir, f'data_backup_{timestamp}.json')
        export_to_json(json_backup)
        
        logger.info(f"Database backup created: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False

def export_to_json(output_file):
    """Export database contents to JSON file."""
    try:
        conn = sqlite3.connect(os.path.join('data', 'database.db'))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all expenses
        cursor.execute('SELECT * FROM expenses')
        expenses = [dict(row) for row in cursor.fetchall()]
        
        # Write to JSON file
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'expenses': expenses
            }, f, indent=2)
        
        conn.close()
        logger.info(f"Data exported to JSON: {output_file}")
    except Exception as e:
        logger.error(f"JSON export failed: {e}")
        raise

def restore_from_backup(backup_file):
    """Restore database from backup file."""
    try:
        # Verify backup file exists
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        # Create backup of current database before restore
        current_backup = os.path.join('data', 'database.db')
        if os.path.exists(current_backup):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pre_restore_backup = os.path.join('data', 'backups', f'pre_restore_{timestamp}.db')
            shutil.copy2(current_backup, pre_restore_backup)
        
        # Restore from backup
        shutil.copy2(backup_file, current_backup)
        logger.info(f"Database restored from backup: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False

def list_backups():
    """List all available database backups."""
    try:
        backup_dir = os.path.join('data', 'backups')
        if not os.path.exists(backup_dir):
            return []
        
        backups = []
        for file in os.listdir(backup_dir):
            if file.startswith('database_backup_') and file.endswith('.db'):
                file_path = os.path.join(backup_dir, file)
                backups.append({
                    'filename': file,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'created': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    except Exception as e:
        logger.error(f"Failed to list backups: {e}")
        return [] 