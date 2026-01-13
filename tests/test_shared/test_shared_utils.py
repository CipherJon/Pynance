# tests/test_shared/test_utils.py

"""
Unit tests for the utils module in the shared module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from shared.utils import validate_input, format_string

class TestUtils(unittest.TestCase):
    """
    Test cases for the utils module.
    """

    def test_validate_input_valid(self):
        """
        Test validating a valid input.
        """
        self.assertTrue(validate_input(100, int))
        self.assertTrue(validate_input(100.0, float))
        self.assertTrue(validate_input("test", str))

    def test_validate_input_invalid(self):
        """
        Test validating an invalid input.
        """
        self.assertFalse(validate_input("not an int", int))
        self.assertFalse(validate_input("not a float", float))

    def test_format_string(self):
        """
        Test formatting a string.
        """
        self.assertEqual(format_string("  test  "), "test")
        self.assertEqual(format_string("  test"), "test")
        self.assertEqual(format_string("test  "), "test")

if __name__ == "__main__":
    unittest.main()
