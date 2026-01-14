# tests/test_pyculator/test_calculator.py

"""
Unit tests for the Calculator class in the pyculator module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from calculator.calculator import Calculator


class TestCalculator(unittest.TestCase):
    """
    Test cases for the Calculator class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.calculator = Calculator()

    def test_add(self):
        """
        Test the add method of the Calculator class.
        """
        result = self.calculator.add(5.0, 3.0)
        self.assertEqual(result, 8.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_subtract(self):
        """
        Test the subtract method of the Calculator class.
        """
        result = self.calculator.subtract(10.0, 4.0)
        self.assertEqual(result, 6.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_multiply(self):
        """
        Test the multiply method of the Calculator class.
        """
        result = self.calculator.multiply(5.0, 3.0)
        self.assertEqual(result, 15.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_divide(self):
        """
        Test the divide method of the Calculator class.
        """
        result = self.calculator.divide(10.0, 2.0)
        self.assertEqual(result, 5.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_divide_by_zero(self):
        """
        Test dividing by zero raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.calculator.divide(10.0, 0.0)

    def test_get_history(self):
        """
        Test retrieving the operation history.
        """
        self.calculator.add(5.0, 3.0)
        self.calculator.subtract(10.0, 4.0)
        history = self.calculator.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("Added 5.0 and 3.0 to get 8.0", history[0])
        self.assertIn("Subtracted 4.0 from 10.0 to get 6.0", history[1])


if __name__ == "__main__":
    unittest.main()
