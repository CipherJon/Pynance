# tests/test_pyculator/test_operations.py

"""
Unit tests for the operations module in the pyculator module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from pyculator.operations import add, subtract, multiply, divide

class TestOperations(unittest.TestCase):
    """
    Test cases for the operations module.
    """

    def test_add(self):
        """
        Test the add function.
        """
        self.assertEqual(add(5.0, 3.0), 8.0)
        self.assertEqual(add(-1.0, 1.0), 0.0)
        self.assertEqual(add(0.0, 0.0), 0.0)

    def test_subtract(self):
        """
        Test the subtract function.
        """
        self.assertEqual(subtract(10.0, 4.0), 6.0)
        self.assertEqual(subtract(5.0, -3.0), 8.0)
        self.assertEqual(subtract(0.0, 0.0), 0.0)

    def test_multiply(self):
        """
        Test the multiply function.
        """
        self.assertEqual(multiply(5.0, 3.0), 15.0)
        self.assertEqual(multiply(-2.0, 3.0), -6.0)
        self.assertEqual(multiply(0.0, 5.0), 0.0)

    def test_divide(self):
        """
        Test the divide function.
        """
        self.assertEqual(divide(10.0, 2.0), 5.0)
        self.assertEqual(divide(-10.0, 2.0), -5.0)
        self.assertEqual(divide(0.0, 5.0), 0.0)

    def test_divide_by_zero(self):
        """
        Test dividing by zero raises a ValueError.
        """
        with self.assertRaises(ValueError):
            divide(10.0, 0.0)

if __name__ == "__main__":
    unittest.main()
