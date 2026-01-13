# tests/test_pybudget/test_budget.py

"""
Unit tests for the Budget class in the pybudget module.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

from pybudget.budget import Budget
from pybudget.expense import Expense


class TestBudget(unittest.TestCase):
    """
    Test cases for the Budget class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.budget = Budget("Test Budget", 1000.0)

    def test_init(self):
        """
        Test the initialization of the Budget class.
        """
        self.assertEqual(self.budget.name, "Test Budget")
        self.assertEqual(self.budget.amount, 1000.0)
        self.assertEqual(len(self.budget.expenses), 0)

    def test_add_expense(self):
        """
        Test adding an expense to the budget.
        """
        expense = Expense("Test Expense", 100.0, "Test Category")
        self.budget.add_expense(expense)
        self.assertEqual(len(self.budget.expenses), 1)
        self.assertEqual(self.budget.expenses[0], expense)

    def test_get_remaining_amount(self):
        """
        Test calculating the remaining amount in the budget.
        """
        expense1 = Expense("Test Expense 1", 200.0, "Test Category 1")
        expense2 = Expense("Test Expense 2", 300.0, "Test Category 2")
        self.budget.add_expense(expense1)
        self.budget.add_expense(expense2)
        remaining = self.budget.get_remaining_amount()
        self.assertEqual(remaining, 500.0)

    def test_get_remaining_amount_no_expenses(self):
        """
        Test calculating the remaining amount when there are no expenses.
        """
        remaining = self.budget.get_remaining_amount()
        self.assertEqual(remaining, 1000.0)

    def test_str_representation(self):
        """
        Test the string representation of the budget.
        """
        budget_str = str(self.budget)
        self.assertIn(
            "Budget(name='Test Budget', amount=1000.0, remaining=", budget_str
        )


if __name__ == "__main__":
    unittest.main()
