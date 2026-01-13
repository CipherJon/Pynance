# tests/test_shared/test_logging.py

"""
Unit tests for the logging module in the shared module.
"""

import logging
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from shared.logging import setup_logging


class TestLogging(unittest.TestCase):
    """
    Test cases for the logging module.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.log_file = os.path.abspath("test_app.log")

    def tearDown(self):
        """
        Clean up after tests.
        """
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_setup_logging(self):
        """
        Test setting up logging.
        """
        setup_logging(self.log_file)
        # Ensure the logging is flushed to the file
        logging.shutdown()
        # Add a small delay to ensure the log file is created
        time.sleep(0.1)
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            log_content = f.read()
            self.assertIn("Logging setup complete.", log_content)


if __name__ == "__main__":
    unittest.main()
