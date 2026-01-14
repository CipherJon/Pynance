import os
import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from file_organizer.utils import (
    FileOperationError,
    FileOrganizerError,
    calculate_file_hash,
    ensure_dir_exists,
    get_date_folder,
    get_file_metadata,
    safe_move_file,
)


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = Path(self.test_dir) / "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("test content")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_ensure_dir_exists(self):
        """Test directory creation."""
        test_subdir = Path(self.test_dir) / "subdir" / "nested"
        ensure_dir_exists(test_subdir)
        self.assertTrue(test_subdir.exists())
        self.assertTrue(test_subdir.is_dir())

    def test_ensure_dir_exists_already_exists(self):
        """Test that existing directory doesn't cause errors."""
        ensure_dir_exists(self.test_dir)
        self.assertTrue(Path(self.test_dir).exists())

    def test_calculate_file_hash(self):
        """Test file hash calculation."""
        file_hash = calculate_file_hash(self.test_file)
        self.assertIsInstance(file_hash, str)
        self.assertEqual(len(file_hash), 64)  # SHA-256 hash length

        # Test with same content
        same_hash = calculate_file_hash(self.test_file)
        self.assertEqual(file_hash, same_hash)

    def test_calculate_file_hash_nonexistent_file(self):
        """Test hash calculation with nonexistent file."""
        with self.assertRaises(FileOperationError):
            calculate_file_hash(Path(self.test_dir) / "nonexistent.txt")

    def test_get_date_folder(self):
        """Test date folder generation."""
        # Test with current file
        date_folder = get_date_folder(self.test_file)
        self.assertIsInstance(date_folder, str)
        self.assertRegex(date_folder, r"^\d{4}-\d{2}$")  # YYYY-MM format

        # Test with use_creation_date=False
        date_folder_modified = get_date_folder(self.test_file, use_creation_date=False)
        self.assertIsInstance(date_folder_modified, str)
        self.assertRegex(date_folder_modified, r"^\d{4}-\d{2}$")

    def test_safe_move_file(self):
        """Test safe file moving."""
        dest_dir = Path(self.test_dir) / "dest"
        dest_dir.mkdir()
        dest_file = dest_dir / "moved_test_file.txt"

        # Move the file
        safe_move_file(self.test_file, dest_file)
        self.assertTrue(dest_file.exists())
        self.assertFalse(self.test_file.exists())

        # Verify content
        with open(dest_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "test content")

    def test_safe_move_file_with_backup(self):
        """Test safe move with existing destination file."""
        dest_dir = Path(self.test_dir) / "dest"
        dest_dir.mkdir()
        dest_file = dest_dir / "test_file.txt"

        # Create destination file first
        with open(dest_file, "w") as f:
            f.write("original content")

        # Move source to destination (should create backup)
        safe_move_file(self.test_file, dest_file)
        self.assertTrue(dest_file.exists())

        # Verify new content
        with open(dest_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "test content")

    def test_get_file_metadata(self):
        """Test file metadata retrieval."""
        metadata = get_file_metadata(self.test_file)
        self.assertIsInstance(metadata, dict)
        self.assertIn("size", metadata)
        self.assertIn("created", metadata)
        self.assertIn("modified", metadata)
        self.assertIn("accessed", metadata)
        self.assertIn("permissions", metadata)

        # Verify metadata types
        self.assertIsInstance(metadata["size"], int)
        self.assertIsInstance(metadata["created"], datetime)
        self.assertIsInstance(metadata["modified"], datetime)
        self.assertIsInstance(metadata["accessed"], datetime)
        self.assertIsInstance(metadata["permissions"], int)

    def test_file_operation_error(self):
        """Test FileOperationError exception."""
        with self.assertRaises(FileOperationError):
            get_file_metadata(Path("/nonexistent/path/to/file.txt"))

    def test_file_organizer_error(self):
        """Test FileOrganizerError base exception."""
        with self.assertRaises(FileOrganizerError):
            raise FileOrganizerError("Test error")


if __name__ == "__main__":
    unittest.main()
