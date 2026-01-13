# tests/test_pybudget/test_expense.py

"""
Unit tests for the Expense class in the pybudget module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from pybudget.expense import Expense


class TestExpense(unittest.TestCase):
    """
    Test cases for the Expense class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.expense = Expense("Test Expense", 100.0, "Test Category")

    def test_init(self):
        """
        Test the initialization of the Expense class.
        """
        self.assertEqual(self.expense.description, "Test Expense")
        self.assertEqual(self.expense.amount, 100.0)
        self.assertEqual(self.expense.category, "Test Category")

    def test_str_representation(self):
        """
        Test the string representation of the expense.
        """
        expense_str = str(self.expense)
        self.assertEqual(
            expense_str,
            "Expense(description='Test Expense', amount=100.0, category='Test Category')",
        )


if __name__ == "__main__":
    unittest.main()
