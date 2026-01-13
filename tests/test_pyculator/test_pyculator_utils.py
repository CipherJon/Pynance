# tests/test_pyculator/test_utils.py

"""
Unit tests for the utils module in the pyculator module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from pyculator.utils import format_number, validate_number


class TestUtils(unittest.TestCase):
    """
    Test cases for the utils module.
    """

    def test_validate_number_valid(self):
        """
        Test validating a valid number.
        """
        self.assertTrue(validate_number(100.0))
        self.assertTrue(validate_number(-100.0))
        self.assertTrue(validate_number(0.0))

    def test_validate_number_invalid(self):
        """
        Test validating an invalid number.
        """
        self.assertFalse(validate_number("not a number"))
        self.assertFalse(validate_number(None))

    def test_format_number(self):
        """
        Test formatting a number as a string.
        """
        self.assertEqual(format_number(100.0), "100.00")
        self.assertEqual(format_number(99.99), "99.99")
        self.assertEqual(format_number(0.0), "0.00")


if __name__ == "__main__":
    unittest.main()
