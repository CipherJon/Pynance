import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from file_organizer.config import (
    BASE_DIR,
    DATE_ORGANIZATION,
    DUPLICATE_HANDLING,
    FILE_TYPES,
)
from file_organizer.utils import (
    FileOperationError,
    FileOrganizerError,
    calculate_file_hash,
    ensure_dir_exists,
    get_date_folder,
    get_file_metadata,
    safe_move_file,
)

logger = logging.getLogger(__name__)


class FileOrganizer:
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize the file organizer with optional base directory."""
        self.base_dir = Path(base_dir) if base_dir else BASE_DIR
        self.known_files: Dict[str, Path] = {}
        self.duplicates_dir: Optional[Path] = None
        self._setup_directories()

    def _setup_directories(self) -> None:
        """Set up necessary directories for organization."""
        try:
            if DUPLICATE_HANDLING.enabled:
                self.duplicates_dir = self.base_dir / DUPLICATE_HANDLING.duplicates_dir
                ensure_dir_exists(self.duplicates_dir)

            # Create category directories
            for category in FILE_TYPES.keys():
                ensure_dir_exists(self.base_dir / category)
        except Exception as e:
            logger.error(f"Failed to set up directories: {str(e)}")
            raise FileOrganizerError("Failed to set up directories") from e

    def _get_file_id(self, file_path: Path) -> str:
        """Get unique identifier for a file based on detection method."""
        try:
            if DUPLICATE_HANDLING.detection_method == "hash":
                return calculate_file_hash(file_path)
            elif DUPLICATE_HANDLING.detection_method == "size":
                return str(file_path.stat().st_size)
            else:  # name
                return file_path.name.lower()
        except Exception as e:
            logger.error(f"Failed to get file ID for {file_path}: {str(e)}")
            raise FileOperationError(f"Failed to get file ID for {file_path}") from e

    def _handle_duplicate(self, file_path: Path, original_path: Path) -> None:
        """Handle duplicate file according to configuration."""
        try:
            if DUPLICATE_HANDLING.handle_duplicates == "move":
                if not self.duplicates_dir:
                    raise FileOrganizerError("Duplicates directory not set up")
                dst_path = self.duplicates_dir / file_path.name
                safe_move_file(file_path, dst_path)
                logger.info(f"Moved duplicate {file_path} to {dst_path}")
            elif DUPLICATE_HANDLING.handle_duplicates == "delete":
                os.remove(file_path)
                logger.info(f"Deleted duplicate {file_path}")
            else:  # keep
                logger.info(f"Keeping duplicate {file_path}")
        except Exception as e:
            logger.error(f"Failed to handle duplicate {file_path}: {str(e)}")
            raise FileOperationError(f"Failed to handle duplicate {file_path}") from e

    def _get_destination_path(self, file_path: Path, category: str) -> Path:
        """Get the destination path for a file, considering date organization."""
        try:
            if DATE_ORGANIZATION.enabled:
                date_folder = get_date_folder(
                    file_path, use_creation_date=DATE_ORGANIZATION.use_creation_date
                )
                return self.base_dir / category / date_folder / file_path.name
            return self.base_dir / category / file_path.name
        except Exception as e:
            logger.error(f"Failed to get destination path for {file_path}: {str(e)}")
            raise FileOperationError(
                f"Failed to get destination path for {file_path}"
            ) from e

    def _process_file(self, file_path: Path) -> Tuple[bool, str]:
        """Process a single file and return success status and message."""
        try:
            if not file_path.is_file():
                return False, f"Skipped {file_path}: Not a file"

            # Check for duplicates
            if DUPLICATE_HANDLING.enabled:
                file_id = self._get_file_id(file_path)
                if file_id in self.known_files:
                    original = self.known_files[file_id]
                    self._handle_duplicate(file_path, original)
                    return True, f"Handled duplicate {file_path}"
                self.known_files[file_id] = file_path

            # Find matching category
            category = "others"
            for cat, extensions in FILE_TYPES.items():
                if file_path.suffix.lower() in extensions:
                    category = cat
                    break

            # Move file to appropriate location
            dst_path = self._get_destination_path(file_path, category)
            safe_move_file(file_path, dst_path)
            return True, f"Moved {file_path} to {dst_path}"

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {str(e)}")
            return False, f"Error processing {file_path}: {str(e)}"

    def organize(self, max_workers: int = 4) -> Dict[str, List[str]]:
        """Organize files in the base directory using parallel processing."""
        results = {"success": [], "failed": []}

        try:
            # Get list of files to process (excluding directories)
            files_to_process = [
                Path(self.base_dir) / f
                for f in os.listdir(self.base_dir)
                if (self.base_dir / f).is_file()
            ]

            if not files_to_process:
                logger.info("No files found to process")
                return results

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {
                    executor.submit(self._process_file, file_path): file_path
                    for file_path in files_to_process
                }

                for future in as_completed(future_to_file):
                    success, message = future.result()
                    if success:
                        results["success"].append(message)
                    else:
                        results["failed"].append(message)

            return results

        except Exception as e:
            logger.error(f"Failed to organize files: {str(e)}")
            raise FileOrganizerError("Failed to organize files") from e


def organize_files(
    base_dir: Optional[Path] = None, max_workers: int = 4
) -> Dict[str, List[str]]:
    """Main function to organize files in the specified directory."""
    try:
        organizer = FileOrganizer(base_dir)
        return organizer.organize(max_workers)
    except Exception as e:
        logger.error(f"Failed to organize files: {str(e)}")
        raise FileOrganizerError("Failed to organize files") from e
