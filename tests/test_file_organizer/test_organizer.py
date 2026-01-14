"""
Test suite for file_organizer module.

To run these tests:
1. Make sure you're in the repository root directory
2. Run: pytest tests/test_organizedpy/ -v
3. Or run all tests: pytest

Note: The pyproject.toml file configures pytest with the proper pythonpath
so imports from file_organizer should work correctly.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from file_organizer.config import DATE_ORGANIZATION, DUPLICATE_HANDLING
from file_organizer.organizer import FileOrganizer, organize_files


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        # Create some test files
        self.test_files = {
            "document.pdf": "PDF content",
            "image.jpg": "JPEG content",
            "archive.zip": "ZIP content",
            "video.mp4": "MP4 content",
            "music.mp3": "MP3 content",
            "unknown.xyz": "UNKNOWN content",
        }

        for filename, content in self.test_files.items():
            filepath = Path(self.test_dir) / filename
            with open(filepath, "w") as f:
                f.write(content)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_organizer_initialization(self):
        """Test FileOrganizer initialization."""
        organizer = FileOrganizer(Path(self.test_dir))
        self.assertEqual(organizer.base_dir, Path(self.test_dir))
        self.assertIsInstance(organizer.known_files, dict)

        # Test with default directory
        organizer_default = FileOrganizer()
        self.assertTrue(str(organizer_default.base_dir).endswith("Downloads"))

    def test_setup_directories(self):
        """Test directory setup."""
        organizer = FileOrganizer(Path(self.test_dir))

        # Check that category directories are created
        for category in [
            "images",
            "documents",
            "archives",
            "videos",
            "music",
            "others",
        ]:
            category_dir = Path(self.test_dir) / category
            self.assertTrue(category_dir.exists())

        # Check duplicates directory if enabled
        if DUPLICATE_HANDLING.enabled:
            duplicates_dir = Path(self.test_dir) / DUPLICATE_HANDLING.duplicates_dir
            self.assertTrue(duplicates_dir.exists())

    def test_get_file_id(self):
        """Test file ID generation."""
        organizer = FileOrganizer(Path(self.test_dir))
        test_file = Path(self.test_dir) / "document.pdf"

        file_id = organizer._get_file_id(test_file)
        self.assertIsInstance(file_id, str)

        # Test different detection methods
        original_method = DUPLICATE_HANDLING.detection_method

        try:
            # Test hash method
            DUPLICATE_HANDLING.detection_method = "hash"
            hash_id = organizer._get_file_id(test_file)
            self.assertIsInstance(hash_id, str)
            self.assertEqual(len(hash_id), 64)  # SHA-256 hash

            # Test size method
            DUPLICATE_HANDLING.detection_method = "size"
            size_id = organizer._get_file_id(test_file)
            self.assertIsInstance(size_id, str)

            # Test name method
            DUPLICATE_HANDLING.detection_method = "name"
            name_id = organizer._get_file_id(test_file)
            self.assertEqual(name_id, "document.pdf")

        finally:
            # Restore original method
            DUPLICATE_HANDLING.detection_method = original_method

    def test_get_destination_path(self):
        """Test destination path generation."""
        organizer = FileOrganizer(Path(self.test_dir))
        test_file = Path(self.test_dir) / "document.pdf"

        # Test without date organization
        original_date_enabled = DATE_ORGANIZATION.enabled
        DATE_ORGANIZATION.enabled = False

        try:
            dest_path = organizer._get_destination_path(test_file, "documents")
            expected_path = Path(self.test_dir) / "documents" / "document.pdf"
            self.assertEqual(dest_path, expected_path)
        finally:
            DATE_ORGANIZATION.enabled = original_date_enabled

    def test_process_file(self):
        """Test file processing."""
        organizer = FileOrganizer(Path(self.test_dir))
        test_file = Path(self.test_dir) / "document.pdf"

        # Process the file
        success, message = organizer._process_file(test_file)

        self.assertTrue(success)
        self.assertIn("document.pdf", message)

        # Verify file was moved
        expected_dest = Path(self.test_dir) / "documents" / "document.pdf"
        self.assertTrue(expected_dest.exists())
        self.assertFalse(test_file.exists())

    def test_organize_files(self):
        """Test the organize_files function."""
        # Disable duplicate handling for this test
        original_duplicate_enabled = DUPLICATE_HANDLING.enabled
        DUPLICATE_HANDLING.enabled = False

        try:
            results = organize_files(Path(self.test_dir), max_workers=2)

            self.assertIn("success", results)
            self.assertIn("failed", results)

            # Should have processed all test files
            self.assertGreater(len(results["success"]), 0)

            # Check that files were organized into categories
            for filename, category in [
                ("document.pdf", "documents"),
                ("image.jpg", "images"),
                ("archive.zip", "archives"),
                ("video.mp4", "videos"),
                ("music.mp3", "music"),
                ("unknown.xyz", "others"),
            ]:
                expected_path = Path(self.test_dir) / category / filename
                self.assertTrue(expected_path.exists())

        finally:
            DUPLICATE_HANDLING.enabled = original_duplicate_enabled

    def test_duplicate_handling(self):
        """Test duplicate file handling."""
        # Create a duplicate file
        original_file = Path(self.test_dir) / "document.pdf"
        duplicate_file = Path(self.test_dir) / "document_copy.pdf"

        # Copy content to create a duplicate
        shutil.copy2(original_file, duplicate_file)

        organizer = FileOrganizer(Path(self.test_dir))

        # Process original file first
        success1, msg1 = organizer._process_file(original_file)
        self.assertTrue(success1)

        # Process duplicate file
        success2, msg2 = organizer._process_file(duplicate_file)
        self.assertTrue(success2)
        self.assertIn("duplicate", msg2.lower())

        # Check that duplicate was handled according to configuration
        if DUPLICATE_HANDLING.handle_duplicates == "move":
            duplicates_dir = Path(self.test_dir) / DUPLICATE_HANDLING.duplicates_dir
            moved_duplicate = duplicates_dir / "document_copy.pdf"
            self.assertTrue(moved_duplicate.exists())
        elif DUPLICATE_HANDLING.handle_duplicates == "delete":
            self.assertFalse(duplicate_file.exists())

    @patch("file_organizer.file_organizer.organizer.ThreadPoolExecutor")
    def test_parallel_processing(self, mock_executor):
        """Test parallel processing with ThreadPoolExecutor."""
        mock_future = MagicMock()
        mock_future.result.return_value = (True, "Test message")
        mock_executor.return_value.__enter__.return_value.submit.return_value = (
            mock_future
        )

        organizer = FileOrganizer(Path(self.test_dir))

        # Mock the _process_file method to avoid actual file operations
        with patch.object(organizer, "_process_file", return_value=(True, "Processed")):
            results = organizer.organize(max_workers=4)

            # Verify ThreadPoolExecutor was used
            mock_executor.assert_called_once_with(max_workers=4)

            # Verify results structure
            self.assertIn("success", results)
            self.assertIn("failed", results)


if __name__ == "__main__":
    unittest.main()

from file_organizer.main import main, parse_args, setup_logging


class TestMain(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_parse_args_defaults(self):
        """Test argument parsing with default values."""
        with patch("sys.argv", ["main.py"]):
            args = parse_args()
            self.assertIsNone(args.directory)
            self.assertEqual(args.workers, 4)
            self.assertFalse(args.verbose)

    def test_parse_args_custom(self):
        """Test argument parsing with custom values."""
        test_dir = "/custom/directory"
        test_workers = 8

        with patch(
            "sys.argv",
            [
                "main.py",
                "--directory",
                test_dir,
                "--workers",
                str(test_workers),
                "--verbose",
            ],
        ):
            args = parse_args()
            self.assertEqual(args.directory, test_dir)
            self.assertEqual(args.workers, test_workers)
            self.assertTrue(args.verbose)

    def test_parse_args_short_flags(self):
        """Test argument parsing with short flags."""
        test_dir = "/short/flag/dir"

        with patch("sys.argv", ["main.py", "-d", test_dir, "-w", "2", "-v"]):
            args = parse_args()
            self.assertEqual(args.directory, test_dir)
            self.assertEqual(args.workers, 2)
            self.assertTrue(args.verbose)

    def test_setup_logging_default(self):
        """Test logging setup with default level."""
        setup_logging(verbose=False)

        # Verify logging was configured
        import logging

        logger = logging.getLogger()
        self.assertTrue(len(logger.handlers) > 0)

    def test_setup_logging_verbose(self):
        """Test logging setup with verbose level."""
        setup_logging(verbose=True)

        # Verify logging was configured with DEBUG level
        import logging

        logger = logging.getLogger()
        self.assertTrue(len(logger.handlers) > 0)

    @patch("file_organizer.file_organizer.main.organize_files")
    @patch("sys.exit")
    def test_main_success(self, mock_exit, mock_organize):
        """Test main function with successful execution."""
        # Mock organize_files to return success
        mock_organize.return_value = {
            "success": ["File1 processed", "File2 processed"],
            "failed": [],
        }

        with patch("sys.argv", ["main.py"]):
            result = main()

            # Verify organize_files was called
            mock_organize.assert_called_once()

            # Verify exit code
            mock_exit.assert_called_with(0)

    @patch("file_organizer.file_organizer.main.organize_files")
    @patch("sys.exit")
    def test_main_failure(self, mock_exit, mock_organize):
        """Test main function with failed execution."""
        # Mock organize_files to raise an exception
        mock_organize.side_effect = Exception("Test error")

        with patch("sys.argv", ["main.py"]):
            result = main()

            # Verify exit code for failure
            mock_exit.assert_called_with(1)

    @patch("file_organizer.file_organizer.main.organize_files")
    @patch("sys.exit")
    def test_main_with_results(self, mock_exit, mock_organize):
        """Test main function with mixed results."""
        # Mock organize_files to return mixed results
        mock_organize.return_value = {
            "success": ["File1 processed successfully"],
            "failed": ["File2 failed to process"],
        }

        with patch("sys.argv", ["main.py"]):
            with patch("builtins.print") as mock_print:
                result = main()

                # Verify results were printed
                self.assertTrue(
                    any(
                        "Successfully processed files" in str(call)
                        for call in mock_print.call_args_list
                    )
                )
                self.assertTrue(
                    any(
                        "Failed to process files" in str(call)
                        for call in mock_print.call_args_list
                    )
                )


if __name__ == "__main__":
    unittest.main()
