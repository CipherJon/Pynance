"""File Organizer Module

A powerful Python tool for organizing files based on their types, dates, and handling duplicates.
"""

from .main import main
from .organizer import organize_files, FileOrganizer
from .config import FILE_TYPES, DUPLICATE_HANDLING, DATE_ORGANIZATION
from .utils import (
    ensure_dir_exists,
    calculate_file_hash,
    get_date_folder,
    safe_move_file,
    get_file_metadata,
    FileOrganizerError,
    FileOperationError
)

__all__ = [
    'main',
    'organize_files',
    'FileOrganizer',
    'FILE_TYPES',
    'DUPLICATE_HANDLING',
    'DATE_ORGANIZATION',
    'ensure_dir_exists',
    'calculate_file_hash',
    'get_date_folder',
    'safe_move_file',
    'get_file_metadata',
    'FileOrganizerError',
    'FileOperationError'
]
