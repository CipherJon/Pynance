import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class DuplicateHandling:
    enabled: bool = True
    detection_method: str = "hash"  # options: name, size, hash
    handle_duplicates: str = "move"  # options: keep, move, delete
    duplicates_dir: str = "_duplicates"


@dataclass
class DateOrganization:
    enabled: bool = False
    use_creation_date: bool = True
    folder_format: str = "monthly"  # options: monthly, quarterly


# Base directory to organize
BASE_DIR: Path = Path(os.path.expanduser("~/Downloads"))

# File types and their corresponding directories
FILE_TYPES: Dict[str, List[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg"],
    "documents": [
        ".pdf",
        ".docx",
        ".txt",
        ".pptx",
        ".xlsx",
        ".odt",
        ".rtf",
        ".csv",
        ".ods",
    ],
    "archives": [".zip", ".tar.gz", ".rar", ".7z", ".bz2"],
    "videos": [".mp4", ".mov", ".mkv", ".avi", ".flv", ".wmv"],
    "music": [".mp3", ".wav", ".ogg", ".flac"],
    "others": [],
}

# Configuration instances
DUPLICATE_HANDLING = DuplicateHandling()
DATE_ORGANIZATION = DateOrganization()

# Logging configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "file_organizer.log",
}
