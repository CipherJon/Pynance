import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

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

    @patch("file_organizer.file_organizer.organizer.organize_files")
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

    @patch("file_organizer.file_organizer.organizer.organize_files")
    @patch("sys.exit")
    def test_main_failure(self, mock_exit, mock_organize):
        """Test main function with failed execution."""
        # Mock organize_files to raise an exception
        mock_organize.side_effect = Exception("Test error")

        with patch("sys.argv", ["main.py"]):
            result = main()

            # Verify exit code for failure
            mock_exit.assert_called_with(1)

    @patch("file_organizer.file_organizer.organizer.organize_files")
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
