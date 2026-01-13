# tests/test_shared/test_config.py

"""
Unit tests for the config module in the shared module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from shared.config import SharedConfig


class TestSharedConfig(unittest.TestCase):
    """
    Test cases for the SharedConfig class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.config = SharedConfig()

    def test_set_setting(self):
        """
        Test setting a configuration setting.
        """
        self.config.set_setting("test_key", "test_value")
        self.assertEqual(self.config.settings["test_key"], "test_value")

    def test_get_setting(self):
        """
        Test retrieving a configuration setting.
        """
        self.config.set_setting("test_key", "test_value")
        value = self.config.get_setting("test_key")
        self.assertEqual(value, "test_value")

    def test_get_nonexistent_setting(self):
        """
        Test retrieving a non-existent configuration setting.
        """
        value = self.config.get_setting("nonexistent_key")
        self.assertIsNone(value)


if __name__ == "__main__":
    unittest.main()
