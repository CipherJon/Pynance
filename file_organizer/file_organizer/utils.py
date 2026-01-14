import hashlib
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .config import LOG_CONFIG

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["level"]),
    format=LOG_CONFIG["format"],
    filename=LOG_CONFIG["file"],
)
logger = logging.getLogger(__name__)


class FileOrganizerError(Exception):
    """Base exception for file organizer errors."""

    pass


class FileOperationError(FileOrganizerError):
    """Exception raised for file operation errors."""

    pass


def ensure_dir_exists(directory: Union[str, Path]) -> None:
    """Ensure that a directory exists, create it if it doesn't."""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {str(e)}")
        raise FileOperationError(f"Failed to create directory {directory}") from e


def calculate_file_hash(file_path: Union[str, Path], block_size: int = 65536) -> str:
    """Calculate SHA-256 hash of a file."""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.error(f"Failed to calculate hash for {file_path}: {str(e)}")
        raise FileOperationError(f"Failed to calculate hash for {file_path}") from e


def get_date_folder(file_path: Union[str, Path], use_creation_date: bool = True) -> str:
    """Get the appropriate date-based folder name for a file."""
    try:
        if use_creation_date:
            timestamp = os.path.getctime(file_path)
        else:
            timestamp = os.path.getmtime(file_path)

        date = datetime.fromtimestamp(timestamp)
        return date.strftime("%Y-%m")
    except Exception as e:
        logger.error(f"Failed to get date folder for {file_path}: {str(e)}")
        raise FileOperationError(f"Failed to get date folder for {file_path}") from e


def safe_move_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """Safely move a file with error handling and logging."""
    try:
        # Ensure destination directory exists
        ensure_dir_exists(os.path.dirname(dst))

        # Create backup before moving
        backup_path = f"{dst}.bak"
        if os.path.exists(dst):
            shutil.copy2(dst, backup_path)

        # Move the file
        shutil.move(src, dst)

        # Verify the move was successful
        if not os.path.exists(dst):
            raise FileOperationError(f"File move verification failed for {dst}")

        # Remove backup if move was successful
        if os.path.exists(backup_path):
            os.remove(backup_path)

        logger.info(f"Successfully moved {src} to {dst}")
    except Exception as e:
        logger.error(f"Failed to move file from {src} to {dst}: {str(e)}")
        # Restore from backup if it exists
        if os.path.exists(backup_path):
            shutil.move(backup_path, dst)
        raise FileOperationError(f"Failed to move file from {src} to {dst}") from e


def get_file_metadata(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Get metadata for a file."""
    try:
        stat = os.stat(file_path)
        return {
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "accessed": datetime.fromtimestamp(stat.st_atime),
            "permissions": stat.st_mode,
        }
    except Exception as e:
        logger.error(f"Failed to get metadata for {file_path}: {str(e)}")
        raise FileOperationError(f"Failed to get metadata for {file_path}") from e
