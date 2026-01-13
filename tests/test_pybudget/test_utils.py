# tests/test_pybudget/test_utils.py

"""
Unit tests for the utils module in the pybudget module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from pybudget.utils import format_currency, validate_amount


class TestUtils(unittest.TestCase):
    """
    Test cases for the utils module.
    """

    def test_validate_amount_positive(self):
        """
        Test validating a positive amount.
        """
        self.assertTrue(validate_amount(100.0))
        self.assertTrue(validate_amount(0.01))

    def test_validate_amount_zero(self):
        """
        Test validating a zero amount.
        """
        self.assertFalse(validate_amount(0.0))

    def test_validate_amount_negative(self):
        """
        Test validating a negative amount.
        """
        self.assertFalse(validate_amount(-100.0))

    def test_format_currency(self):
        """
        Test formatting a number as a currency string.
        """
        self.assertEqual(format_currency(100.0), "$100.00")
        self.assertEqual(format_currency(99.99), "$99.99")
        self.assertEqual(format_currency(0.0), "$0.00")


if __name__ == "__main__":
    unittest.main()
